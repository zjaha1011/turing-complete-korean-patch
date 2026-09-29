import unittest,tempfile,sys
from pathlib import Path
from patcher import Installer,InstallLock,digest,menu_patch,safe

class PatcherTests(unittest.TestCase):
 def test_concurrent_install_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   with InstallLock(Path(tmp)):
    with self.assertRaises(RuntimeError):
     with InstallLock(Path(tmp)):pass
   with InstallLock(Path(tmp)):pass
 def test_signature_and_idempotency(self):
  before=b'MZ test Svenska (3% done) end';after=before.replace(b'Svenska (3% done)','한국어(Korean)'.encode())
  cfg={'before':'Svenska (3% done)','after':'한국어(Korean)','original_sha256':[digest(before)],'patched_sha256':[digest(after)]}
  self.assertEqual(menu_patch(before,cfg)[0],after);self.assertEqual(menu_patch(after,cfg)[0],after)
  for bad in (b'MZ none',before+before,before+b'new version',after+after):self.assertIsNone(menu_patch(bad,cfg)[0])
 def test_backup_repair_uninstall(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/'text').write_bytes(b'original');i=Installer(root)
   i.write('text',b'korean');i.write('added',b'new');backup=i.entries['text']['backup']
   i.write('text',b'korean');self.assertEqual(backup,i.entries['text']['backup'])
   (root/'text').write_bytes(b'Steam update')
   with self.assertRaises(RuntimeError):i.write('text',b'korean')
   i.write('text',b'korean',repair=True)
   self.assertEqual((root/backup).read_bytes(),b'original')
   i.uninstall();self.assertEqual((root/'text').read_bytes(),b'Steam update');self.assertFalse((root/'added').exists())
 def test_uninstall_preserves_later_edits(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);i=Installer(root);i.write('text',b'ours');(root/'text').write_bytes(b'user edit')
   i.uninstall();self.assertEqual((root/'text').read_bytes(),b'user edit')
 def test_manual_copy_has_no_fake_backup(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/'text').write_bytes(b'korean');i=Installer(root);i.write('text',b'korean')
   self.assertEqual(i.entries,{})
 def test_path_escape_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   with self.assertRaises(ValueError):safe(Path(tmp),'../escape')
 def test_corrupt_backup_not_restored(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/'text').write_bytes(b'original');i=Installer(root);i.write('text',b'korean')
   (root/i.entries['text']['backup']).write_bytes(b'corrupt')
   with self.assertRaises(IOError):i.uninstall()
   self.assertEqual((root/'text').read_bytes(),b'korean')
if __name__=='__main__':unittest.main()
