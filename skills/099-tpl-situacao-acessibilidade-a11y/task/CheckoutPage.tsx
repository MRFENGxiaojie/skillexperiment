import React, { useState } from "react";
import "./checkout.css";

/**
 * 结账页（摘要版，保留全部已知无障碍问题，行号以本文件为准）
 */
export default function CheckoutPage() {
  const [cart, setCart] = useState([
    { name: "无线机械键盘", qty: 1, price: 399 },
    { name: "Type-C 数据线", qty: 2, price: 39 },
  ]);
  const [showConfirm, setShowConfirm] = useState(false);
  const [banners] = useState([0, 1, 2]);

  // 顶部自动轮播 banner（无暂停、无手动切换、无焦点控制）
  const [bannerIdx, setBannerIdx] = useState(0);

  // 自动轮播，每 3 秒切换一次
  React.useEffect(() => {
    const timer = setInterval(() => {
      setBannerIdx((i) => (i + 1) % banners.length);
    }, 3000);
    return () => clearInterval(timer);
  }, []);

  return (
    <main className="checkout">
      {/* 无跳转链接（skip link） */}
      <section className="banner-carousel" aria-hidden={false}>
        {banners.map((b, i) => (
          <div key={b} className={i === bannerIdx ? "banner active" : "banner"}>
            年中大促第{i + 1}波，结算立减
          </div>
        ))}
      </section>

      <h1>购物车</h1>
      <table className="cart-table">
        {/* 无 <thead>，表格没有表头 */}
        <tr>
          <td>商品</td>
          <td>单价</td>
          <td>数量</td>
          <td>小计</td>
        </tr>
        {cart.map((item) => (
          <tr key={item.name}>
            <td>{item.name}</td>
            <td>¥{item.price}</td>
            <td>{item.qty}</td>
            <td>¥{item.price * item.qty}</td>
          </tr>
        ))}
      </table>

      <img src="/images/checkout-hero.jpg" alt="image" className="hero" />

      <h2>收货信息</h2>
      <div className="field">
        {/* 只有 placeholder，没有 label */}
        <input type="text" placeholder="收货人姓名" />
      </div>
      <div className="field">
        <input type="tel" placeholder="手机号码" />
      </div>
      <div className="field">
        <input type="text" placeholder="省 / 市 / 区" />
      </div>
      <div className="field">
        <textarea placeholder="详细地址（街道、门牌号）"></textarea>
        {/* 帮助文字 #999999 白底，对比度不足 */}
        <span className="hint">信息仅用于本次配送，不会外泄。</span>
      </div>

      {/* “提交订单”不是按钮，而是 div + onClick */}
      <div
        className="submit-order"
        role={undefined}
        onClick={() => setShowConfirm(true)}
      >
        提交订单
      </div>

      {/* 订单确认弹窗：打开/关闭无焦点管理 */}
      {showConfirm && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>确认订单</h2>
            <p>共 {cart.length} 件商品，合计 ¥{cart.reduce((s, i) => s + i.price * i.qty, 0)}</p>
            <div className="modal-actions">
              <span className="btn" onClick={() => setShowConfirm(false)}>
                返回修改
              </span>
              <button onClick={() => alert("支付跳转（示意）")}>去支付</button>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
