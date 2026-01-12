import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Permite que o servidor seja acessado fora do container (essencial para o Docker)
    host: '0.0.0.0',
    // Define a porta para 5173 (deve ser a mesma que você mapeou no docker-compose)
    port: 5173,
    // Garante que o Hot Module Replacement (HMR) funcione corretamente através do Docker
    watch: {
      usePolling: true,
    },
  },
})