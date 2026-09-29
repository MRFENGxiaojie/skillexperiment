import React, { useState } from 'react';

interface Order {
  id: string;
  count: number;
  createdAt: string;
  status: 'pending' | 'paid';
}

export default function Orders({ orders }: { orders: Order[] }) {
  const [keyword, setKeyword] = useState('');
  const filtered = orders.filter(o => o.id.includes(keyword));

  return (
    <div>
      <h1>订单列表</h1>
      <input placeholder="搜索订单号" value={keyword} onChange={e => setKeyword(e.target.value)} />
      <button style={{ marginLeft: 8 }}>导出</button>
      <table>
        <thead>
          <tr><th>订单号</th><th>数量</th><th>创建时间</th><th>状态</th></tr>
        </thead>
        <tbody>
          {filtered.map(o => (
            <tr key={o.id}>
              <td>{o.id}</td>
              <td>{o.count} 条订单</td>
              <td>{new Date(o.createdAt).toLocaleString()}</td>
              <td>{o.status === 'paid' ? '已支付' : '待支付'}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {filtered.length === 0 && <p>没有找到订单</p>}
      <button style={{ paddingRight: 12 }}>删除选中</button>
    </div>
  );
}
