import React, { useState } from 'react';

const mockProductionData = [
  {
    id: 1,
    productName: 'Tea',
    quantity: 1000,
    pricePerUnit: 1.5,
    totalValue: 1500,
    date: '2024-08-10'
  },
  {
    id: 2,
    productName: 'Milk',
    quantity: 800,
    pricePerUnit: 1.2,
    totalValue: 960,
    date: '2024-07-25'
  },
  {
    id: 3,
    productName: 'Tomatoes',
    quantity: 600,
    pricePerUnit: 2.0,
    totalValue: 1200,
    date: '2024-08-15'
  }
];

const mockTransactionData = [
  {
    id: 1,
    date: '2024-08-01',
    description: 'Payment Received',
    type: 'Credit',
    amount: 2000
  },
  {
    id: 2,
    date: '2024-08-05',
    description: 'Purchase of Seeds',
    type: 'Debit',
    amount: 500
  },
  {
    id: 3,
    date: '2024-08-10',
    description: 'Sale of Tea',
    type: 'Credit',
    amount: 1500
  }
];

function Dashboard() {
  const [productionData, setProductionData] = useState(mockProductionData);
  const [transactionData] = useState(mockTransactionData); // No need for setState as it's static
  const [filter, setFilter] = useState('');
  const [sortBy, setSortBy] = useState('date');

  const handleSort = (field) => {
    const sortedData = [...productionData].sort((a, b) => (a[field] > b[field] ? 1 : -1));
    setProductionData(sortedData);
    setSortBy(field);
  };

  const handleFilter = (e) => {
    setFilter(e.target.value);
  };

  const filteredProductionData = productionData.filter(item =>
    item.productName.toLowerCase().includes(filter.toLowerCase())
  );

  const downloadStatement = () => {
    const csvContent = [
      ['Product Name', 'Quantity', 'Price per Unit', 'Total Value', 'Date'],
      ...filteredProductionData.map(item => [
        item.productName,
        item.quantity,
        item.pricePerUnit,
        item.totalValue,
        item.date
      ])
    ].map(e => e.join(',')).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', 'production_statement.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="dashboard">
      <div className="credit-limit">
        <h2>Credit Limit</h2>
        <p>Your credit limit is Ksh.10,000</p>
      </div>
      <div className="create-data-buttons">
        <button>Borrow</button>
        <button>Transact</button>
        <button>Produce</button>
      </div>
      <h1>Production Data</h1>
      <div className="controls">
        <input
          type="text"
          placeholder="Filter by product"
          value={filter}
          onChange={handleFilter}
        />
        <button onClick={() => handleSort('productName')}>Sort by Product Name</button>
        <button onClick={() => handleSort('date')}>Sort by Date</button>
        <button onClick={downloadStatement}>Download Statement</button>
      </div>
      <table className="production-table">
        <thead>
          <tr>
            <th>Product Name</th>
            <th>Quantity</th>
            <th>Price per Unit</th>
            <th>Total Value</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {filteredProductionData.map(item => (
            <tr key={item.id}>
              <td>{item.productName}</td>
              <td>{item.quantity}</td>
              <td>{item.pricePerUnit.toFixed(2)}</td>
              <td>{item.totalValue.toFixed(2)}</td>
              <td>{item.date}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Transaction History</h2>
      <div className="controls">
        <input
          type="text"
          placeholder="Filter by product"
          value={filter}
          onChange={handleFilter}
        />
        <button onClick={() => handleSort('productName')}>Sort by Product Name</button>
        <button onClick={() => handleSort('date')}>Sort by Date</button>
        <button onClick={downloadStatement}>Download Statement</button>
      </div>
      <table className="transaction-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Description</th>
            <th>Type</th>
            <th>Amount</th>
          </tr>
        </thead>
        <tbody>
          {transactionData.map(transaction => (
            <tr key={transaction.id}>
              <td>{transaction.date}</td>
              <td>{transaction.description}</td>
              <td>{transaction.type}</td>
              <td>{transaction.amount.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Dashboard;
