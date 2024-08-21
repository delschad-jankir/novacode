import { Breadcrumbs } from '@/components/breadcrumbs';
import { ProjectForm } from '@/components/forms/project-form';
import PageContainer from '@/components/layout/page-container';
import React from 'react';

const breadcrumbItems = [
  { title: 'Dashboard', link: '/dashboard' },
  { title: 'Projects', link: '/dashboard/projects' },
  { title: 'Create', link: '/dashboard/projects/create' }
];
export default function Page() {
  return (
    <PageContainer scrollable={true}>
      <div className="space-y-4">
        <Breadcrumbs items={breadcrumbItems} />
        <ProjectForm
          categories={[
            { _id: 'shirts', name: 'shirts' },
            { _id: 'pants', name: 'pants' }
          ]}
          initialData={null}
          key={null}
        />
      </div>
    </PageContainer>
  );
}
