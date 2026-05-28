#!/usr/bin/env node
// Entry point for the CDK app. Filled in by Module 05 (orchestrator) onward.
// TODO: replace process.env.CDK_DEFAULT_ACCOUNT with a pinned account ID per environment.
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { ResearchCopilotStack } from '../lib/research-copilot-stack';

const app = new cdk.App();

new ResearchCopilotStack(app, 'ResearchCopilotStack', {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: 'us-east-1',
  },
});
