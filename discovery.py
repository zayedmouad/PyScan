#!/usr/bin/python3
import platform
import subprocess


def build_ping_command(ip: str, os_name: str):
  if os_name == "windows":
    return ["ping", "-n", "1", "-w", "2000", ip]
  if os_name == "darwin":
    return ["ping", "-c", "1", "-W", "2000", ip]
  return ["ping", "-c", "1", "-W", "2", ip]


def is_host_alive(ip: str, wait_timeout: float = 3.0):
  os_name = platform.system().lower()
  cmd = build_ping_command(ip, os_name)

  proc = subprocess.Popen(
      cmd,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      text=True,
  )

  try:
    out, err = proc.communicate(timeout=wait_timeout)
    combined = (out + "\n" + err).lower()

    if proc.returncode == 0:
      return "host is alive"
    if "unreachable" in combined or "no route" in combined:
      return "host is unreachable"
    return "host is unreachable (no reply or ICMP blocked)"
  except subprocess.TimeoutExpired:
    proc.terminate()
    try:
      proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
      proc.kill()
      proc.wait()
    return "host is unreachable (timed out)"


def main():
  ip = input("Enter the target IP address: ").strip()
  message = is_host_alive(ip)
  print(f"{ip} -> {message}")


if __name__ == "__main__":
  main()
