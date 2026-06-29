# 04 - Serverless Architecture

> *"No server is easier to manage than no server." - Werner Vogels, CTO of Amazon*

This section explores the pinnacle of Cloud Computing abstraction: Serverless. Serverless does not mean there are no servers; it means you no longer provision, scale, or manage them.

## 📂 Contents

### 1. [Event-Driven Architectures](./event-driven-architectures.md)
The core philosophy of Serverless. Systems that react to events rather than running continuously.
- What is an Event?
- Producers, Routers, and Consumers
- The Choreography vs. Orchestration debate
- AWS Step Functions vs EventBridge

### 2. The Serverless Ecosystem (Covered in Deep Dive)
- Compute: [AWS Lambda](../02-aws-deep-dive/aws-lambda.md)
- Database: [Amazon DynamoDB](../02-aws-deep-dive/aws-dynamodb.md)
- Storage: [Amazon S3](../02-aws-deep-dive/aws-s3.md)
- API Gateway: [Amazon API Gateway](../02-aws-deep-dive/aws-api-gateway.md)

---

## 🎯 Learning Objectives

By the end of this section, you will be able to:
1. Explain the difference between "Always-On" compute (EC2) and "Event-Driven" compute (Lambda).
2. Design a fully serverless, highly scalable web application that costs exactly $0.00 when there are no users.
3. Understand the trade-offs of Serverless (Cold Starts, Vendor Lock-in) and when NOT to use it.
