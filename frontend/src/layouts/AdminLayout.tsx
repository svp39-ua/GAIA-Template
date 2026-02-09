// [Feature: News Management] [Story: NM-ADM-001] [Ticket: NM-ADM-001-FE-T03]
import { Outlet } from "react-router-dom"
import { Toaster } from "sonner"

export default function AdminLayout() {
    return (
        <div className="min-h-screen bg-background font-sans antialiased text-foreground">
            <header className="border-b h-14 flex items-center px-6 bg-card">
                <div className="font-bold text-lg text-primary mr-8">GAIA Admin</div>
                <nav className="flex gap-4 text-sm font-medium">
                    <a href="/admin/news/create" className="hover:text-primary">Noticias</a>
                    <a href="#" className="hover:text-primary text-muted-foreground">Usuarios</a>
                </nav>
            </header>
            <main className="p-6">
                <Outlet />
            </main>
            <Toaster />
        </div>
    )
}
