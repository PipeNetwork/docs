# Mainnet Storage API

Pipe Storage exposes an S3-compatible object API through its gateway. Customer credit is purchased with USDC on **Solana mainnet**. Node staking and customer storage accounts are separate: using storage does not require operating a node or holding a 10,000 PIPE position.

## Fund the Account and Create Credentials

1. Open the [storage workspace](https://pipe.love/storage), connect your Solana wallet, and sign the storage-account login message.
2. Hold mainnet USDC for the purchase and SOL for the wallet's network fee. Review the amount and recipient displayed by the wallet before signing the purchase.
3. Wait for finalized payment verification and the credit balance to update. If a payment remains pending, use the saved-payment status or resume action for the same invoice; an interrupted browser response does not mean the transfer failed.
4. In **S3 access**, create a credential limited to your intended bucket, optional object prefix, and required operations. Record its secret when displayed; it cannot be recovered later.
5. Copy the S3 endpoint supplied for your account. The [service reference](https://pipe.love/storage/docs) also lists the gateway configuration. Use path-style addressing and an explicit region such as `us-east-1`.

Follow the amount limits and purchase availability displayed by the workspace. A node enrollment invite or control-plane administrator token is not an S3 credential.

## Upload and Download with AWS CLI

Install AWS CLI, then configure a dedicated profile with the access key and secret created above. This avoids changing another application's profile:

```bash
aws configure --profile pipe-mainnet
aws configure set s3.addressing_style path --profile pipe-mainnet
export AWS_PROFILE=pipe-mainnet
export AWS_DEFAULT_REGION=us-east-1
export AWS_REQUEST_CHECKSUM_CALCULATION=when_required
export AWS_RESPONSE_CHECKSUM_VALIDATION=when_required
read -r -p 'S3 gateway endpoint shown for your account: ' PIPE_S3_ENDPOINT
read -r -p 'Bucket allowed by your credential: ' PIPE_BUCKET
export PIPE_S3_ENDPOINT PIPE_BUCKET
```

Use a credential with write, read, and list permissions for this walkthrough. If it is restricted to a prefix, include that prefix in each object key:

```bash
aws --endpoint-url "$PIPE_S3_ENDPOINT" s3api create-bucket --bucket "$PIPE_BUCKET"
printf 'Hello from Pipe mainnet\n' > pipe-example.txt
aws --endpoint-url "$PIPE_S3_ENDPOINT" s3 cp pipe-example.txt "s3://$PIPE_BUCKET/pipe-example.txt"
aws --endpoint-url "$PIPE_S3_ENDPOINT" s3 ls "s3://$PIPE_BUCKET/"
aws --endpoint-url "$PIPE_S3_ENDPOINT" s3 cp "s3://$PIPE_BUCKET/pipe-example.txt" pipe-downloaded.txt
cmp pipe-example.txt pipe-downloaded.txt
```

An existing bucket does not need to be created again. Delete the example object with the singular object API when finished:

```bash
aws --endpoint-url "$PIPE_S3_ENDPOINT" s3api delete-object \
  --bucket "$PIPE_BUCKET" --key pipe-example.txt
```

Uploads and downloads consume credit. Use the account's usage view to inspect the actual charges.

## Python Example

With `boto3` installed, reuse the profile and environment from the CLI example:

```python
import os
import boto3
from botocore.config import Config

s3 = boto3.Session(profile_name="pipe-mainnet").client(
    "s3",
    endpoint_url=os.environ["PIPE_S3_ENDPOINT"],
    region_name="us-east-1",
    config=Config(
        signature_version="s3v4",
        s3={"addressing_style": "path"},
        request_checksum_calculation="when_required",
        response_checksum_validation="when_required",
    ),
)
bucket = os.environ["PIPE_BUCKET"]
s3.put_object(Bucket=bucket, Key="hello.txt", Body=b"hello")
response = s3.get_object(Bucket=bucket, Key="hello.txt")
with response["Body"] as body:
    assert body.read() == b"hello"
s3.delete_object(Bucket=bucket, Key="hello.txt")
```

## Authentication and Supported Operations

Requests use AWS Signature Version 4 with scoped S3 credentials. Ordinary fixed-payload requests can also use presigned URLs. Treat presigned URLs as access credentials for their scope and lifetime.

| Area | Supported operations |
| --- | --- |
| Buckets | Create, HEAD, and delete a bucket; ListObjectsV2 within credential scope. |
| Objects | PUT, GET, HEAD, singular DELETE, conditional requests, and byte ranges. |
| Multipart | CreateMultipartUpload, UploadPart, ListParts, CompleteMultipartUpload, AbortMultipartUpload, and ListMultipartUploads. |
| Streaming writes | Signed `STREAMING-AWS4-HMAC-SHA256-PAYLOAD` bodies for PutObject and UploadPart. |

Use `If-None-Match: *` to create an object only if its key is absent. Use `If-Match` with the returned ETag to protect replacement against a changed object. A failed precondition returns `412 PreconditionFailed`.

Pipe ETags are quoted **BLAKE3** identities. Treat them as opaque values; they do not match AWS MD5 or multipart-MD5 calculations.

## Billing and Credit

The account tracks available, reserved, and spent credit. A reservation holds budget while an operation is in progress; inspect the final usage and invoice state to reconcile it. Customer prepaid balances are distinct from recognized net protocol revenue.

Writes account for stored bytes and replication work. Reads account for bytes served to the customer. Multipart part writes and the final object materialization are billed independently. Completing a multipart upload can therefore require additional available credit even after all parts have uploaded. Retry or replacement of an object request is separate from resuming the same payment invoice.

Multipart uploads retain parts until they are completed or aborted. Abort unused uploads instead of assuming they will disappear under an automatic lifecycle rule. Revoking a credential does not delete its objects.

Check the service's current rates and account usage rather than applying the former node-payment rates to customer bills. **No customer charge creates a reward or payout for an individual storage node.**

## Compatibility Limits

The documented S3 contract has these limits:

- A single explicit byte-range read is limited to 32 MiB. Split larger ranges into supported windows.
- Versioning, lifecycle rules, object lock/retention, managed server-side encryption, and KMS are not supported. Apply client-side encryption before upload when your application requires it.
- Batch `DeleteObjects` is not supported. Use singular `DeleteObject`; clients that always batch deletions require a different deletion command.
- SigV4a, presigned streaming bodies, streaming trailer signatures, and checksum trailers are not supported. The CLI and Python examples above disable optional checksum behavior that relies on unsupported trailers.
- AWS-specific ETag assumptions are not supported. Use the ETag returned by Pipe for conditional requests.

Unsupported operations return S3 `NotImplemented`. The implemented S3 subset and deployment limits apply even when using an otherwise compatible AWS client.

## Rotate or Revoke Credentials

Use **S3 access** in the storage workspace to create a replacement with the same required scope, update the application, verify access, and revoke the old credential. Store secrets outside source control and browser bundles. Revocation stops future authorization; it does not erase stored data or cancel an already signed payment.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Signature or access failure | Endpoint, explicit region, system clock, credential status, bucket/prefix scope, and requested permissions. |
| Insufficient credit | Available balance, outstanding reservations, and the completion cost of a multipart upload. |
| Pending payment | Resume or check the same saved invoice and signature in the workspace. |
| `NotImplemented` | Whether the client sent an unsupported operation, checksum trailer, or batch delete. |
| Range request refused | Keep each explicit byte range within the documented 32 MiB limit. |
| ETag mismatch in application code | Treat the returned BLAKE3 ETag as opaque instead of calculating an MD5 ETag. |

See the [storage overview](overview.md), [mainnet node guide](../nodes/mainnet.md), and [tokenomics policy](../Tokenomics.md) for the other parts of the system.
