import PageTransition from '../components/PageTransition';

export default function Settings() {
  return (
    <PageTransition>
      <div className="px-4 py-8">
        <h1 className="text-xl font-semibold text-gray-900">Settings</h1>
        <p className="mt-4 text-gray-500">User settings configuration will appear here.</p>
      </div>
    </PageTransition>
  );
}