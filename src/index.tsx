import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './app'; // Import the Intro component

export function renderToDom(container: HTMLElement) {
  const root = createRoot(container); // Create a root.

  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
}

const container = document.getElementById('app');
if (container) {
  renderToDom(container);
} else {
  console.error('Failed to find the root container');
}