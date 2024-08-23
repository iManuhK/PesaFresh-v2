import React, { useState, useEffect } from 'react';
import { getMyCredits } from '../api';

function Dashboard() {
  const [filter, setFilter] = useState('');
  const [sortBy, setSortBy] = useState('date');
  const [myTransactions, setMyTransactions] = useState([]);
  const [myProductions, setMyProductions] = useState([]);
  const [myCredit, setCredits] = useState([]);

  useEffect(() => {
    // Fetch transactions data
    const fetchTransactions = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5555/dashboard/my-transactions`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('jwt_Token')}`,
          },
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setMyTransactions(data);
      } catch (error) {
        console.error('Error fetching transactions:', error);
      }
    };
    fetchTransactions();
  }, []);

  useEffect(() => {
    // Fetch productions data
    const fetchProductions = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5555/dashboard/my-productions`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('jwt_Token')}`,
          },
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setMyProductions(data);
      } catch (error) {
        console.error('Error fetching productions:', error);
      }
    };
    fetchProductions();
  }, []);

useEffect(() => {
  const fetchCredits = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5555/dashboard/my-credits', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('jwt_Token')}`,
        },
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setCredits(data);
      console.log(data);
    } catch (error) {
      console.error('Failed to fetch credits:', error);
    }
  };
  fetchCredits();
}, []);

  const handleSort = (field) => {
    const sortedData = [...myProductions].sort((a, b) => (a[field] > b[field] ? 1 : -1));
    setMyProductions(sortedData);
    setSortBy(field);
  };

  const handleFilter = (e) => {
    setFilter(e.target.value);
  };

  const filteredProductionData = myProductions.filter((item) =>
    item.product.product_name.toLowerCase().includes(filter.toLowerCase())
  );

  const downloadStatement = () => {
    const csvContent = [
      ['Date', 'Product Name', 'Quantity', 'Factory'],
      ...filteredProductionData.map(item => [
        item.date,
        item.product.product_name,
        item.production_in_UOM.toFixed(2),
        item.industry.industry_name,
      ]),
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
      <div className="user-identity">
        <h1>Welcome <span>UserX</span></h1>
      </div>
      <div className="credit-limit">
        <h2>Credit Limit</h2>
        <p>Your credit limit is Ksh. <span>10,000</span></p>
      </div>
      <div className="loans">
        <h2>Active Loan Amount Ksh. <span>5,000</span></h2>
        <p>Status</p>
        <h2>Borrowing History</h2>
        <div className="controls">
          <button onClick={() => handleSort('date')}>Sort by Date</button>
          <button onClick={downloadStatement}>Download Statement</button>
        </div>
        <table className="borrowing-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Currency</th>
              <th>Amount Borrowed</th>
              <th>Amount Paid</th>
              <th>Remaining Amount</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
          {myCredit.length > 0 ? (
            myCredit.map(credit => {
              const totalPayments = credit.payment.reduce((sum, payment) => sum + payment.amount, 0);
              return (
                <tr key={credit.id}>
                  <td>{credit.date_borrowed}</td>
                  <td>{credit.currency}</td>
                  <td>{credit.amount_borrowed.toFixed(2)}</td>
                  <td>{totalPayments.toFixed(2)}</td>
                  <td>{(credit.amount_borrowed - totalPayments).toFixed(2)}</td>
                  <td>{credit.payment_status}</td>
                </tr>
              );
            })
          ) : (
            <tr>
              <td colSpan="7" style={{ textAlign: 'center' }}>No Data Available!</td>
            </tr>
          )}
        </tbody>

        </table>
      </div>
      <div className="create-data-buttons">
        <button>Borrow</button>
        <button>Transact</button>
        <button>Produce</button>
      </div>
      <h2>Production Data</h2>
      <div className="controls">
        <input
          type="text"
          placeholder="Filter by product"
          value={filter}
          onChange={handleFilter}
        />
        <button onClick={() => handleSort('product_id')}>Sort by Product Name</button>
        <button onClick={() => handleSort('date')}>Sort by Date</button>
        <button onClick={downloadStatement}>Export to Excel</button>
      </div>
      <table className="production-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Product Name</th>
            <th>Quantity</th>
            <th>Factory</th>
          </tr>
        </thead>
        <tbody>
          {filteredProductionData.length > 0 ? (
            filteredProductionData.map(item => (
              <tr key={item.id}>
                <td>{item.date}</td>
                <td>{item.product.product_name}</td>
                <td>{item.production_in_UOM.toFixed(2)}</td>
                <td>{item.industry.industry_name}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="4" style={{ textAlign: 'center' }}>No Data Available!</td>
            </tr>
          )}
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
        <button onClick={() => handleSort('date')}>Sort by Date</button>
        <button onClick={downloadStatement}>Download Statement</button>
      </div>
      <table className="transaction-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Currency</th>
            <th>Description</th>
            <th>Type</th>
            <th>Amount</th>
          </tr>
        </thead>
        <tbody>
          {myTransactions.length > 0 ? (
            myTransactions.map(transaction => (
              <tr key={transaction.id}>
                <td>{transaction.transaction_date}</td>
                <td>{transaction.currency}</td>
                <td>{transaction.description}</td>
                <td>{transaction.transaction_type}</td>
                <td>{transaction.amount.toFixed(2)}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="5" style={{ textAlign: 'center' }}>No Data Available!</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Dashboard;
