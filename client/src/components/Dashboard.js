import * as React from 'react';
import { useState } from 'react';
import { DataGrid, GridToolbar } from '@mui/x-data-grid';

export default function Dashboard() {
const [data, setData]= useState("data");
const [loading, setLoading] = useState(true);

  return (
    <div style={{ height: 300, width: '100%' }}>
      <DataGrid {...data} loading={loading} slots={{ toolbar: GridToolbar }} />
    </div>
  );
}
