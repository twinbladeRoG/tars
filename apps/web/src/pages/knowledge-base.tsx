import { Title } from '@mantine/core';

import UserDocumentList from '@/components/modules/knowledge-base/UserDocumentList';

const KnowledgeBasePage = () => {
  return (
    <div>
      <Title order={4} mb="md">
        Documents
      </Title>

      <UserDocumentList />
    </div>
  );
};

export default KnowledgeBasePage;
