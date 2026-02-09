// [Feature: News Management] [Story: NM-ADM-001] [Ticket: NM-ADM-001-FE-T03]
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import AdminLayout from '@/layouts/AdminLayout'
import CreateNewsPage from '@/features/news/pages/CreateNewsPage'

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          {/* Redirect root to admin news create for now since it's the only page */}
          <Route path="/" element={<Navigate to="/admin/news/create" replace />} />

          <Route path="/admin" element={<AdminLayout />}>
            <Route path="news/create" element={<CreateNewsPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App
