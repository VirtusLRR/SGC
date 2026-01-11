import { useState, useRef } from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from '../Sidebar';
import { ChatbotWidget } from '../../features/chatbot/components/chatbot-widget/ChatbotWidget';
import './AppLayout.css';

export const AppLayout = () => {
  const inventoryRef = useRef(null);

  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const contentRef = useRef(null);

  const handleToggleSidebar = () => {
    setIsSidebarCollapsed(prev => !prev);
  };

  const handleChatbotResponse = () => {
    // Chama o método loadData do InventoryOverview após resposta do chatbot
    if (inventoryRef.current && inventoryRef.current.loadData) {
        inventoryRef.current.loadData();
    }
  };

  const menuItems = [
    { path: '/items', icon: '📦', label: 'Itens' },
    { path: '/recipes', icon: '📝', label: 'Receitas' },
    { path: '/statistics', icon: '📊', label: 'Estatísticas' }
  ];

  return (
    <div className="app-layout">
      <Sidebar
        items={menuItems}
        isCollapsed={isSidebarCollapsed}
        onToggle={handleToggleSidebar}
      />
      <main
        className={`app-layout__content ${isSidebarCollapsed ? 'app-layout__content--expanded' : ''}`}
        ref={contentRef}
      >
        <Outlet context={{ inventoryRef, onRefresh: handleChatbotResponse }} />
      </main>
      <ChatbotWidget onResponseReceived={handleChatbotResponse} />
    </div>
  );
};

