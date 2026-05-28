// Empty stack scaffold. Resources (S3, OpenSearch, Bedrock KB, Lambda, IAM)
// are added incrementally starting in Module 05.
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';

export class ResearchCopilotStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // TODO: ingestion bucket (Module 02)
    // TODO: OpenSearch Serverless collection (Module 03)
    // TODO: Bedrock Knowledge Base (Module 06)
    // TODO: orchestrator Lambda + IAM (Module 05)
    // TODO: Guardrails (Module 07)
    // TODO: AgentCore wiring (Module 08)
  }
}
