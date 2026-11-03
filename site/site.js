'use strict';
document.documentElement.classList.add('js');
const checklist = document.getElementById('review-checklist');
if (checklist) {
  const checks = [...checklist.querySelectorAll('input[type="checkbox"]')];
  const output = document.getElementById('review-progress');
  const update = () => {
    const count = checks.filter(input => input.checked).length;
    output.textContent = count === checks.length
      ? count + ' of ' + checks.length + ' review prompts marked. The authors still make the final decision.'
      : count + ' of ' + checks.length + ' review prompts marked.';
  };
  checklist.addEventListener('change', update);
  checklist.addEventListener('reset', () => setTimeout(update, 0));
  update();
}
document.querySelectorAll('[data-copy]').forEach(button => {
  button.addEventListener('click', async () => {
    const target = document.getElementById(button.dataset.copy);
    const status = button.nextElementSibling;
    try {
      if (!navigator.clipboard || !window.isSecureContext) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(target.textContent);
      status.textContent = 'Request copied.';
    } catch (_) {
      const range = document.createRange();
      range.selectNodeContents(target);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent = 'Text selected. Use your device’s copy command.';
    }
  });
});
