import { InventoryOverview } from './features/items/views/InventoryOverview'
import { ChatbotWidget } from './features/chatbot/components/chatbot-widget/ChatbotWidget'
import './App.css'

function App() {
  return (
    <div className="app">
      <InventoryOverview />
      <ChatbotWidget />
    </div>
  )
}

export default App
