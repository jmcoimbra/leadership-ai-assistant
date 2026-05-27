# Canonical Pattern: Browser-Facing S3 Buckets

**Added:** 2026-05-25
**Last Updated:** 2026-05-25
**Source:** JULI-255 (Drata Test 104 failure on `[your-org]-merchant-fonts`)

**Owner:** [Brain Owner] | **Pillar:** Pillar 4 (Embrace AI at every level) - App Preview infra hardening | **Measurable Outcome:** Drata Test 104 passing for every public-asset S3 bucket in the production AWS account | **Escalation Trigger:** Any new bucket in `[your-org]-devops/production/` or `[your-org]-devops/staging-new/` that sets `block_public_policy=false` or `restrict_public_buckets=false`

> Cross-references: `cloud-security.md` (defense in depth, least privilege), `compliance-evidence.md` (Drata controls), `aws-cloud-architecture.md`

---

## Decision (JULI-255, 2026-05-25)

**Pattern A - CloudFront + Origin Access Control + private bucket** is the canonical pattern for any S3 bucket serving browser-readable content in the [Your Company] production AWS account.

Reverses the JULI-107 "no CloudFront" decision for storage-hardening reasons. The original JULI-107 reasoning ("license attestation is the legal gate, not URL signing") stands: CF + OAC does not URL-sign, does not gate license enforcement, and does not change the public-readability model. It only removes the bucket's anonymous-read surface so Drata Test 104 (Cloud Storage Public Access Disabled) passes.

## Why not Pattern B (BPA on + bucket policy)

JULI-255 audit found Pattern B as written in the ticket is technically incoherent. `restrict_public_buckets = true` neutralizes any bucket policy with `Principal: "*"` - AWS evaluates anonymous access against the restriction and denies. You cannot have full BPA on AND anonymous browser reads via policy. Pattern B is off the table for every browser-facing bucket.

## Why not Pattern C (Drata exception)

Recurring compliance review forever. SOC2 auditor scrutiny on the business justification. Sets a precedent for additional exception requests as more browser-facing buckets land. Permanent fix (Pattern A) costs one-time engineering work; exception costs permanent review overhead.

## Required Configuration

### S3 bucket (Terraform)

```hcl
resource "aws_s3_bucket_public_access_block" "<bucket>" {
  bucket                  = aws_s3_bucket.<bucket>.id
  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

data "aws_iam_policy_document" "<bucket>-cloudfront-read" {
  statement {
    sid       = "AllowCloudFrontServicePrincipal"
    effect    = "Allow"
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.<bucket>.arn}/<scoped-prefix>/*"]
    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "AWS:SourceArn"
      values   = [aws_cloudfront_distribution.<bucket>.arn]
    }
  }
}
```

### CloudFront distribution

```hcl
resource "aws_cloudfront_origin_access_control" "<bucket>" {
  name                              = "<bucket>-oac"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "<bucket>" {
  enabled         = true
  is_ipv6_enabled = true
  price_class     = "PriceClass_100"

  origin {
    domain_name              = aws_s3_bucket.<bucket>.bucket_regional_domain_name
    origin_id                = "S3-<bucket>"
    origin_access_control_id = aws_cloudfront_origin_access_control.<bucket>.id
  }

  default_cache_behavior {
    target_origin_id       = "S3-<bucket>"
    allowed_methods        = ["GET", "HEAD", "OPTIONS"]
    cached_methods         = ["GET", "HEAD", "OPTIONS"]
    viewer_protocol_policy = "redirect-to-https"
    compress               = true

    # CachingOptimized (managed) - respects origin Cache-Control
    cache_policy_id            = "658327ea-f89d-4fab-a63d-7e88639e58f6"
    # CORS-S3Origin (managed) - forwards Origin + Access-Control-Request-* to S3
    origin_request_policy_id   = "88a5eaf4-2fd4-4709-b370-b4c650ea3fcf"
    # Custom CORS + security headers policy (see resource below)
    response_headers_policy_id = aws_cloudfront_response_headers_policy.<bucket>.id
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}
```

### Response headers policy (CORS + security)

The cache + origin-request policies above use AWS-managed UUIDs. The response
headers policy is custom because the AWS-managed `SimpleCORS` policy emits
only the Access-Control-Allow-* headers; combining it with browser security
headers (HSTS, X-Content-Type-Options nosniff, Referrer-Policy) requires a
custom resource. Same one-time setup per distribution:

```hcl
resource "aws_cloudfront_response_headers_policy" "<bucket>" {
  name = "<bucket>-cors-security"

  cors_config {
    access_control_allow_credentials = false
    access_control_allow_headers { items = ["*"] }
    access_control_allow_methods { items = ["GET", "HEAD"] }
    access_control_allow_origins { items = ["*"] }
    access_control_max_age_sec       = 600
    origin_override                  = true
  }

  security_headers_config {
    strict_transport_security {
      access_control_max_age_sec = 31536000
      include_subdomains         = true
      preload                    = true
      override                   = true
    }
    content_type_options { override = true }
    referrer_policy {
      referrer_policy = "strict-origin-when-cross-origin"
      override        = true
    }
  }
}
```

HSTS uses the strictest directives. `include_subdomains` and `preload` are
functionally no-ops while the distribution lives on the AWS-owned
`.cloudfront.net` host (no subdomains served, only Amazon can submit the parent
zone to the preload list), but they are the secure-by-default choice and start
carrying weight without a tf change if the pattern ever migrates to a custom
domain. Satisfies checkov CKV_AWS_259.

## Constants (AWS Managed Policy IDs)

- `CachingOptimized` (cache policy): `658327ea-f89d-4fab-a63d-7e88639e58f6`
- `CORS-S3Origin` (origin request policy): `88a5eaf4-2fd4-4709-b370-b4c650ea3fcf`

## DNS Decision

Default `<distribution-id>.cloudfront.net` URL is the canonical browser-facing endpoint. No custom DNS, no ACM cert. Keeps the JULI-107 "no Route 53 record" decision. Custom DNS may be added later if branded URLs become a product requirement.

## Rollout Sequencing

Replacing a public bucket with CF + OAC is a two-PR operation:

1. **Additive PR**: add CF distribution, OAC, and CF-principal bucket policy statement alongside the existing anonymous-read statement. BPA stays as-is. Both access paths work.
2. **Frontend cutover**: point the FE at the CF domain via env var. Verify content loads.
3. **Hardening PR**: remove the anonymous-read statement, flip BPA all-true. Drata 104 passes.

Skipping step 2 between PRs risks an outage if the FE has not been redeployed before BPA flips.

## Applies To

- `[your-org]-merchant-fonts` (prod) - JULI-255 in progress
- `[your-org]-staging-merchant-fonts` (staging + sandbox tenants) - JULI-255 in progress
- Any future bucket landing in `[your-org]-devops/{production,staging-new}/` with browser-readable content
