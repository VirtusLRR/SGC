import { useRef } from 'react'
import { InventoryOverview } from './features/items/views/InventoryOverview'
import { ChatbotWidget } from './features/chatbot/components/chatbot-widget/ChatbotWidget'
import './App.css'

function App() {
  const inventoryRef = useRef(null);

  const handleChatbotResponse = () => {
    // Chama o método loadData do InventoryOverview após resposta do chatbot
    if (inventoryRef.current && inventoryRef.current.loadData) {
      inventoryRef.current.loadData();
    }
  };

  return (
    <div className="app">
      <InventoryOverview ref={inventoryRef} />
      <ChatbotWidget onResponseReceived={handleChatbotResponse} />
    </div>
  )
}

export default App
