import { useState, useRef } from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from '../Sidebar';
import { ChatbotWidget } from '../../features/chatbot/components/chatbot-widget/ChatbotWidget';
import './AppLayout.css';

export const AppLayout = () => {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const contentRef = useRef(null);

  const handleToggleSidebar = () => {
    setIsSidebarCollapsed(prev => !prev);
  };

  const handleChatbotResponse = () => {
    console.log('Chatbot recebeu resposta - views podem atualizar dados');
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
        <Outlet context={{ contentRef, onRefresh: handleChatbotResponse }} />
      </main>
      <ChatbotWidget onResponseReceived={handleChatbotResponse} />
    </div>
  );
};

