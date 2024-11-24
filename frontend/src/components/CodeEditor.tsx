import React, { useEffect, useState } from 'react';
import { Box, Paper, Toolbar, IconButton, Typography } from '@mui/material';
import { PlayArrow, Save, Refresh } from '@mui/icons-material';
import Editor, { Monaco } from '@monaco-editor/react';
import { useDispatch } from 'react-redux';
import { executeCode, saveCode } from '../store/codeSlice';

interface CodeEditorProps {
  fileId?: string;
  initialContent?: string;
  language?: string;
  readOnly?: boolean;
  onContentChange?: (content: string) => void;
}

export const CodeEditor: React.FC<CodeEditorProps> = ({
  fileId,
  initialContent = '',
  language = 'python',
  readOnly = false,
  onContentChange
}) => {
  const [content, setContent] = useState(initialContent);
  const [isExecuting, setIsExecuting] = useState(false);
  const dispatch = useDispatch();

  const handleEditorChange = (value: string = '') => {
    setContent(value);
    onContentChange?.(value);
  };

  const handleExecute = async () => {
    setIsExecuting(true);
    try {
      await dispatch(executeCode({ content, language }));
    } finally {
      setIsExecuting(false);
    }
  };

  const handleSave = async () => {
    if (fileId) {
      await dispatch(saveCode({ fileId, content }));
    }
  };

  const handleEditorDidMount = (editor: any, monaco: Monaco) => {
    monaco.editor.defineTheme('customTheme', {
      base: 'vs-dark',
      inherit: true,
      rules: [],
      colors: {
        'editor.background': '#1E1E1E'
      }
    });
    monaco.editor.setTheme('customTheme');
  };

  return (
    <Paper sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Toolbar variant="dense">
        <IconButton 
          onClick={handleExecute} 
          disabled={isExecuting || readOnly}
          title="Execute Code"
        >
          <PlayArrow />
        </IconButton>
        <IconButton 
          onClick={handleSave}
          disabled={!fileId || readOnly}
          title="Save File"
        >
          <Save />
        </IconButton>
        <Typography variant="body2" sx={{ ml: 2 }}>
          {fileId || 'Untitled'}
        </Typography>
      </Toolbar>
      <Box sx={{ flexGrow: 1 }}>
        <Editor
          height="100%"
          defaultLanguage={language}
          value={content}
          onChange={handleEditorChange}
          options={{
            readOnly,
            minimap: { enabled: false },
            fontSize: 14,
            lineNumbers: 'on',
            roundedSelection: false,
            scrollBeyondLastLine: false,
            automaticLayout: true
          }}
          onMount={handleEditorDidMount}
        />
      </Box>
    </Paper>
  );
}; 