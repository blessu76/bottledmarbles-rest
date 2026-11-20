"""GA4 local-host guard, run for real: the inline snippet from scripts/chrome.py ga_head() is executed under node
with a stubbed location/document, and we check whether it appends the gtag.js <script>.

Local hosts (no gtag.js): localhost, 127.x, [::1], 0.0.0.0, 10.x, 192.168.x, 172.16–31.x, 169.254.x.x, *.local,
IPv6 unique-local [fc00::/7] and link-local [fe80::/10] (brackets included), empty hostname (file://).
Public hosts (gtag.js appended): the real domain, and the neighbours of the private ranges (172.15, 172.32, 11.x, 192.169.x),
plus names that only start like a private IP (10.example.com, 100.x, 10abc.com, 172.16.example.com).
Run: python3 -m unittest discover -s tests -q   (skipped when node is not installed)
"""
import json
import re
import shutil
import subprocess
import unittest

import helpers  # noqa: F401  (puts scripts/ on sys.path)
import chrome

LOCAL = ["localhost", "127.0.0.1", "127.9.9.9", "[::1]", "0.0.0.0", "10.0.0.5", "192.168.1.20",
         "172.16.0.1", "172.20.3.4", "172.31.255.1", "10.255.255.255", "192.168.0.0", "",
         # IPv6 loopback / unique-local fc00::/7 / link-local fe80::/10 (location.hostname keeps the brackets)
         "[fc00::1]", "[fd12:3456:789a::1]", "[fdff::1]", "[fe80::1]", "[febf::1]", "[FE80::1]",
         # *.local (mDNS names), link-local 169.254.x.x
         "mac.local", "my-printer.local", "169.254.0.1", "169.254.255.254"]
PUBLIC = ["bottledmarbles.ipe.rest", "ipe.rest", "1.1.1.1", "172.15.0.1", "172.32.0.1", "11.0.0.1",
          "192.169.0.1", "100.64.0.1", "100.1.2.3", "110.0.0.1", "10.example.com", "10abc.com", "10.0.0",
          "172.16.example.com", "192.168.example.com", "127.example.com", "1.10.0.1",
          # public names that only start like a private/local form
          "local.example.com", "mylocal", "localhost.example.com", "example.local.com",
          "169.253.0.1", "169.255.0.1", "1690.254.0.1",
          # IPv6 outside the local ranges: fbff (below fc00), fe00 (below fe80), fec0 (above fe80/10), global 2001:db8
          "[fbff::1]", "[fe00::1]", "[fec0::1]", "[2001:db8::1]"]

HARNESS = """
const hostname = %s;
const appended = [];
global.location = { hostname };
global.document = {
  head: { appendChild(s) { appended.push(s.src); } },
  createElement() { return {}; },
};
global.window = {};
%s
console.log(JSON.stringify(appended));
"""


def snippet_body():
    m = re.search(r"<script>(.*)</script>", chrome.ga_head(), re.S)
    return m.group(1)


@unittest.skipUnless(shutil.which("node"), "node not installed")
class GaGuardRuntime(unittest.TestCase):
    def loads_gtag(self, hostname):
        code = HARNESS % (json.dumps(hostname), snippet_body())
        out = subprocess.run(["node", "-e", code], capture_output=True, text=True, timeout=20)
        self.assertEqual(out.returncode, 0, out.stderr)
        return bool(json.loads(out.stdout.strip() or "[]"))

    def test_local_hosts_do_not_load_gtag(self):
        for host in LOCAL:
            self.assertFalse(self.loads_gtag(host), "should be skipped: %r" % host)

    def test_public_hosts_load_gtag(self):
        for host in PUBLIC:
            self.assertTrue(self.loads_gtag(host), "should load gtag: %r" % host)


class GaGuardSource(unittest.TestCase):
    def test_guard_text_is_in_the_snippet_before_the_loader(self):
        body = snippet_body()
        self.assertLess(body.index("return;"), body.index("createElement"))
        self.assertLess(body.index("return;"), body.index("googletagmanager.com/gtag/js"))


if __name__ == "__main__":
    unittest.main()
