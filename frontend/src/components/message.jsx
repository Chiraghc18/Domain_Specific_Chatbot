// src/components/Message.jsx
import React from 'react';
import ReactMarkdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';
import remarkGfm from 'remark-gfm';
import dompurify from 'dompurify';

const allowedTags = [
  'p', 'br', 'strong', 'em', 'h1', 'h2', 'h3', 
  'ul', 'ol', 'li', 'a', 'blockquote', 'code', 'pre'
];

const Message = ({ text, sender }) => {
  const sanitize = (dirty) => {
    return dompurify.sanitize(dirty, {
      ALLOWED_TAGS: allowedTags,
      ALLOWED_ATTR: ['href', 'target']
    });
  };

  return (
    <div className={`message ${sender}`}>
      <ReactMarkdown
        rehypePlugins={[rehypeRaw]}
        remarkPlugins={[remarkGfm]}
        components={{
          a: ({ node, ...props }) => (
            <a {...props} target="_blank" rel="noopener noreferrer" />
          )
        }}
      >
        {sanitize(text)}
      </ReactMarkdown>
    </div>
  );
};

export default Message;