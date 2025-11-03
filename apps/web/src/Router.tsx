import { createBrowserRouter } from 'react-router';
import { RouterProvider } from 'react-router/dom';

import RootLayout from './components/modules/shared/RootLayout';
import NotFound from './components/NotFound';
import AgentPage from './pages/agent';
import CandidatesPage from './pages/candidates';
import DocumentsPage from './pages/documents';
import KnowledgeBasePage from './pages/knowledge-base';
import LoginPage from './pages/login';
import Home from './pages';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />,
  },
  {
    path: '/',
    element: <RootLayout />,
    errorElement: <div>Not Found</div>,
    children: [
      { path: '/agent', element: <AgentPage /> },
      {
        path: '/knowledge-base',
        element: <KnowledgeBasePage />,
      },
      {
        path: '/documents',
        element: <DocumentsPage />,
      },
      { path: '/candidates', element: <CandidatesPage /> },
    ],
  },
  {
    path: '/login',
    element: <LoginPage />,
  },
  { path: '*', element: <NotFound /> },
]);

const Router = () => <RouterProvider router={router} />;

export default Router;
