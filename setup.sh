#!/bin/bash

# Create project directories
mkdir -p ai-agent-system/{backend,frontend,workspace}
mkdir -p ai-agent-system/backend/{app,tests,config}
mkdir -p ai-agent-system/backend/app/{agents,tools,models,core,api}
mkdir -p ai-agent-system/frontend/{src,public}
mkdir -p ai-agent-system/frontend/src/{components,pages,store,utils}
mkdir -p ai-agent-system/workspace/{projects,outputs}

# Initialize backend
cd ai-agent-system/backend
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-dotenv langchain openai redis celery

# Initialize frontend
cd ../frontend
npm init -y
npm install react react-dom typescript @mui/material @emotion/react @emotion/styled @reduxjs/toolkit react-redux socket.io-client @monaco-editor/react 