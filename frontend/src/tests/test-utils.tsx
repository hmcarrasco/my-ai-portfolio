import { render } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { ThemeProvider } from '../contexts/ThemeContext';
import { ChatProvider } from '../contexts/ChatContext';
import { DocsProvider } from '../contexts/DocsContext';
import type { ReactElement } from 'react';

export function renderWithProviders(ui: ReactElement, { route = '/' } = {}) {
  return render(
    <ThemeProvider>
      <ChatProvider>
        <DocsProvider>
          <MemoryRouter initialEntries={[route]}>{ui}</MemoryRouter>
        </DocsProvider>
      </ChatProvider>
    </ThemeProvider>
  );
}
