const agents = [
  { name: 'Claude Code', icon: 'claude' },
  { name: 'OpenAI Codex', icon: 'openai' },
  { name: 'Cursor', icon: 'cursor' },
  { name: 'Gemini CLI', icon: 'google' },
  { name: 'Windsurf', icon: 'windsurf' },
  { name: 'DeepSeek', icon: 'deepseek' },
  { name: 'Perplexity', icon: 'perplexity' },
  { name: 'Ollama', icon: 'ollama' },
];

const agentTrack = document.querySelector('#agentTrack');
const agentMarquee = document.querySelector('#agentMarquee');
const copyButton = document.querySelector('#copyInstallCommand');
const installCommand = document.querySelector('#installCommand');
const copyStatus = document.querySelector('#copyStatus');

function createAgentGroup(isDuplicate = false) {
  const group = document.createElement('div');
  group.className = 'agent-group';
  group.setAttribute('role', 'list');
  if (isDuplicate) group.setAttribute('aria-hidden', 'true');

  agents.forEach((agent) => {
    const item = document.createElement('div');
    item.className = 'agent-item';
    item.setAttribute('role', 'listitem');

    const icon = document.createElement('img');
    icon.src = `https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/${agent.icon}.svg`;
    icon.alt = '';
    icon.loading = 'lazy';
    icon.addEventListener('error', () => icon.remove());

    const label = document.createElement('span');
    label.textContent = agent.name;
    item.append(icon, label);
    group.append(item);
  });

  return group;
}

agentTrack.append(createAgentGroup(), createAgentGroup(true));
agentMarquee.addEventListener('focusin', () => {
  agentTrack.style.animationPlayState = 'paused';
});
agentMarquee.addEventListener('focusout', () => {
  agentTrack.style.animationPlayState = '';
});

async function copyCommand() {
  const command = installCommand.textContent.trim();
  try {
    await navigator.clipboard.writeText(command);
  } catch {
    const temporaryInput = document.createElement('textarea');
    temporaryInput.value = command;
    temporaryInput.setAttribute('readonly', '');
    temporaryInput.style.position = 'fixed';
    temporaryInput.style.opacity = '0';
    document.body.append(temporaryInput);
    temporaryInput.select();
    const copied = document.execCommand('copy');
    temporaryInput.remove();
    if (!copied) {
      copyStatus.textContent = 'Copy failed. Select the command to copy it.';
      return;
    }
  }

  copyButton.textContent = 'Copied';
  copyStatus.textContent = 'Installation command copied.';
  window.setTimeout(() => {
    copyButton.textContent = 'Copy';
    copyStatus.textContent = '';
  }, 1800);
}

copyButton.addEventListener('click', copyCommand);
