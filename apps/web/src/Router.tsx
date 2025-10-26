import { createBrowserRouter } from 'react-router';
import { RouterProvider } from 'react-router/dom';

import AgentPage from './pages/agent';
import KnowledgeBasePage from './pages/knowledge-base';
import Home from './pages';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />,
  },
  {
    path: '/agent',
    element: <AgentPage />,
  },
  {
    path: '/knowledge-base',
    element: <KnowledgeBasePage />,
  },
]);

const Router = () => <RouterProvider router={router} />;

export default Router;
