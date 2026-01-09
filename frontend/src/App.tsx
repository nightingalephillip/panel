import { Routes, Route, Navigate } from 'react-router-dom';
import { LoginPage, RegisterPage, ProtectedRoute } from '@/modules/auth';
import { MainLayout } from '@/layouts';

function App() {
  return (
    <Routes>
      {/* Auth routes */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* Protected routes */}
      <Route
        path="/cases"
        element={
          <ProtectedRoute>
            <MainLayout>
              <CasesPlaceholder />
            </MainLayout>
          </ProtectedRoute>
        }
      />

      {/* Dashboard redirect */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Navigate to="/cases" replace />
          </ProtectedRoute>
        }
      />

      {/* 404 */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

// Placeholder until Cases module is built
function CasesPlaceholder() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold text-gray-100 mb-4">Cases</h1>
      <p className="text-gray-400">Cases module coming in Phase 4...</p>
    </div>
  );
}

function NotFound() {
  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-white mb-4">404</h1>
        <p className="text-gray-400">Page not found</p>
      </div>
    </div>
  );
}

export default App;
