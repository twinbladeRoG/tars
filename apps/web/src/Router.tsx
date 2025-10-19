import { createBrowserRouter } from 'react-router';
import { RouterProvider } from 'react-router/dom';

import AgentPage from './pages/agent';
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
]);

const Router = () => <RouterProvider router={router} />;

export default Router;
