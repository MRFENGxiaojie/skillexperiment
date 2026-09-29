// 云仓科技官网交互脚本（含已知无障碍问题，供审计参考）

(function () {
  "use strict";

  // ── 轮播图：自动播放，无暂停/停止机制，无 aria 标注 ──
  var carousel = document.getElementById("hero-carousel");
  var slides = [];
  var current = 0;
  var timer = null;

  if (carousel) {
    slides = carousel.querySelectorAll(".carousel-slide");
    timer = window.setInterval(function () {
      current = (current + 1) % slides.length;
      showSlide(current);
    }, 3500);
  }

  function showSlide(idx) {
    for (var i = 0; i < slides.length; i++) {
      slides[i].classList.toggle("active", i === idx);
    }
  }

  // 全局函数：轮播箭头按钮 onclick 调用（按钮无 aria-label）
  window.moveSlide = function (delta) {
    if (!slides.length) return;
    current = (current + delta + slides.length) % slides.length;
    showSlide(current);
  };

  // ── 订阅表单：无 label、错误仅用 alert 提示 ──
  var newsletterForm = document.getElementById("newsletter-form");
  if (newsletterForm) {
    newsletterForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var input = newsletterForm.querySelector('input[name="email"]');
      var value = input.value.trim();
      if (!value || value.indexOf("@") < 0) {
        window.alert("请输入有效的邮箱地址");
        return;
      }
      input.value = "";
      window.alert("订阅成功，感谢关注！");
    });
  }

  // ── 结算表单：校验失败时错误汇总面板更新，但不移动焦点、无 aria-live ──
  var checkoutForm = document.getElementById("checkout-form");
  if (checkoutForm) {
    checkoutForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var errors = [];
      var receiver = checkoutForm.querySelector('input[name="receiver"]');
      var phone = checkoutForm.querySelector('input[name="phone"]');
      var province = checkoutForm.querySelector('select[name="province"]');
      var address = checkoutForm.querySelector('textarea[name="address"]');

      if (!receiver.value.trim()) errors.push("请填写收货人姓名");
      if (!/^1\d{10}$/.test(phone.value.trim())) errors.push("请填写有效的手机号码");
      if (!province.value) errors.push("请选择省份");
      if (!address.value.trim()) errors.push("请填写详细地址");

      var summary = document.getElementById("error-summary");
      if (errors.length) {
        summary.hidden = false;
        summary.textContent = errors.join("；");
      } else {
        summary.hidden = true;
        window.alert("订单已提交（演示环境，未实际下单）");
      }
    });
  }
})();
