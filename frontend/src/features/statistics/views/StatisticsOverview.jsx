import { MetricCard } from '../../../components';
import {
  BarChart3,
  DollarSign,
  AlertTriangle,
  TrendingDown,
} from 'lucide-react';
import {
  PeriodSelector,
  StatisticsChart,
  ConsumptionTable,
  TopItemsCard,
  TransactionsList,
  MonthlyExpensesCard,
} from '../components';
import { useStatistics } from '../hooks/useStatistics';
import { CHART_COLORS } from '../types/statistics.types';
import './StatisticsOverview.css';

/**
 * Página principal de estatísticas e dashboard
 */
export const StatisticsOverview = () => {
  const {
    period,
    summary,
    dailyTransactions,
    mostTransacted,
    consumptionRate,
    recentTransactions,
    monthlyExpenses,
    loading,
    error,
    fetchAllStatistics,
    fetchMonthlyExpenses,
    changePeriod,
  } = useStatistics(30);


  const handlePeriodChange = (newPeriod) => {
    changePeriod(newPeriod);
  };


  // Calcular métricas para os cards
  const totalTransactions = summary?.total_transactions || 0;
  const totalValue = summary?.total_value || 0;
  const lowStockItems = consumptionRate?.filter(item =>
    item.dias_para_esgotamento !== null && item.dias_para_esgotamento < 7
  ).length || 0;
  const avgConsumption = consumptionRate?.length > 0
    ? (consumptionRate.reduce((sum, item) => sum + (item.taxa_diaria || 0), 0) / consumptionRate.length).toFixed(2)
    : 0;

  // Preparar dados para o gráfico de transações diárias
  const dailyChartData = (dailyTransactions || []).map(item => ({
    date: new Date(item.date).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' }),
    Entradas: item.entrada || 0,
    Saídas: item.saida || 0,
  }));

  // Preparar dados para o gráfico de top itens
  const topItemsChartData = (mostTransacted || []).slice(0, 10).map(item => ({
    name: item.item_name?.length > 20 ? item.item_name.substring(0, 20) + '...' : (item.item_name || 'N/A'),
    quantidade: item.total_quantity || 0,
  }));

  if (error) {
    return (
      <div className="statistics-overview">
        <div className="statistics-overview__error">
          <span className="statistics-overview__error-icon">
            <AlertTriangle size={48} />
          </span>
          <h2>Erro ao carregar estatísticas</h2>
          <p>{error}</p>
          <button
            className="statistics-overview__retry-button"
            onClick={fetchAllStatistics}
          >
            Tentar novamente
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="statistics-overview">
      {/* Header */}
      <div className="statistics-overview__header">
        <div className="statistics-overview__title-wrapper">
          <BarChart3 size={28} className="statistics-overview__title-icon" />
          <div>
            <h1 className="statistics-overview__title">Dashboard de Estatísticas</h1>
            <p className="statistics-overview__subtitle">
              Visão geral das transações e consumo de itens
            </p>
          </div>
        </div>
        <PeriodSelector selectedPeriod={period} onPeriodChange={handlePeriodChange} />
      </div>

      {/* KPIs - Métricas Principais */}
      <div className="statistics-overview__metrics">
        <MetricCard
          title="Total de Transações"
          value={totalTransactions}
          icon={<BarChart3 size={32} />}
          loading={loading}
          subtitle={`Últimos ${period} dias`}
        />
        <MetricCard
          title="Valor Movimentado"
          value={`R$ ${totalValue.toFixed(2)}`}
          icon={<DollarSign size={32} />}
          loading={loading}
          subtitle="Total no período"
        />
        <MetricCard
          title="Itens Críticos"
          value={lowStockItems}
          icon={<AlertTriangle size={32} />}
          type={lowStockItems > 0 ? 'warning' : 'success'}
          loading={loading}
          subtitle="Estoque < 7 dias"
        />
        <MetricCard
          title="Taxa Média de Consumo"
          value={avgConsumption}
          icon={<TrendingDown size={32} />}
          loading={loading}
          subtitle="unidades/dia"
        />
      </div>

      {/* Gastos Mensais */}
      <div className="statistics-overview__monthly">
        <MonthlyExpensesCard
          monthlyData={monthlyExpenses}
          loading={loading}
          onLoad={fetchMonthlyExpenses}
        />
      </div>

      {/* Gráficos Principais */}
      <div className="statistics-overview__charts">
        <StatisticsChart
          type="line"
          title="Transações Diárias"
          data={dailyChartData}
          dataKeys={[
            { key: 'Entradas', color: CHART_COLORS.success, name: 'Entradas' },
            { key: 'Saídas', color: CHART_COLORS.danger, name: 'Saídas' },
          ]}
          xAxisKey="date"
          height={300}
          loading={loading}
        />
        <StatisticsChart
          type="bar"
          title="Top 10 Itens Mais Transacionados"
          data={topItemsChartData}
          dataKeys={[
            { key: 'quantidade', color: CHART_COLORS.primary, name: 'Quantidade' },
          ]}
          xAxisKey="name"
          height={300}
          loading={loading}
        />
      </div>

      {/* Análises Detalhadas */}
      <div className="statistics-overview__details">
        <ConsumptionTable data={consumptionRate} loading={loading} />
        <TopItemsCard items={mostTransacted} type="all" limit={10} loading={loading} />
      </div>

      {/* Transações Recentes */}
      <div className="statistics-overview__recent">
        <TransactionsList
          transactions={recentTransactions}
          limit={10}
          loading={loading}
        />
      </div>
    </div>
  );
};

