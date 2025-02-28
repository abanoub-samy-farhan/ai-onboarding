import React from "react";
import Link from "next/link";

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-white shadow-md p-6 hidden md:block">
        <h2 className="text-xl font-bold mb-6">Banking Dashboard</h2>
        <nav className="space-y-4">
          <Link href="/dashboard" className="block text-gray-700 hover:text-blue-500">
            🏠 Dashboard
          </Link>
          <Link href="/transactions" className="block text-gray-700 hover:text-blue-500">
            💳 Transactions
          </Link>
          <Link href="/settings" className="block text-gray-700 hover:text-blue-500">
            ⚙️ Settings
          </Link>
        </nav>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col">
        {/* Navbar */}
        <header className="bg-white shadow p-4 flex justify-between items-center">
          <h2 className="text-lg font-semibold">Welcome</h2>
          <button className="text-red-500 font-semibold">Logout</button>
        </header>

        {/* Content */}
        <main className="flex-1 p-6">{children}</main>
      </div>
    </div>
  );
};

export default Layout;
