import pathlib
import tarfile
import tempfile
import typing

import conflictify

def do_test(test_name:str, expected_conflicts:typing.List[pathlib.Path]):
	test_tar_path = pathlib.Path(__file__).parent / "resources" / ("%s.tar" % test_name)
	with tempfile.TemporaryDirectory() as test_checkout_directory:
		test_checkout_path = pathlib.Path(test_checkout_directory)
		with tarfile.TarFile(str(test_tar_path)) as test_tar_file:
			test_tar_file.extractall(str(test_checkout_path))
		actual_conflicts = conflictify.find_conflicting_files(test_checkout_path, "master", "feature")
		assert expected_conflicts == actual_conflicts

def test_plaintext():
	do_test(
		"plaintext",
		[
			{
				conflictify.FilePathSource.MERGE_BASE: conflictify.ConflictingFile(conflictify.FilePathSource.MERGE_BASE, 100755, "e01de952a5bc6b79382611c57cbebf65c5fbc2e3", pathlib.Path("file.py")),
				conflictify.FilePathSource.BASE: conflictify.ConflictingFile(conflictify.FilePathSource.BASE, 100755, "00abec391bc1a657caef025dbef50b06dba0084a", pathlib.Path("file.py")),
				conflictify.FilePathSource.HEAD: conflictify.ConflictingFile(conflictify.FilePathSource.HEAD, 100755, "489e4f2ec57119c8ef7e0574ee39edeccf7d304f", pathlib.Path("file.py")),
			},
		],
	)

def test_binary():
	do_test(
		"binary",
		[
			{
				conflictify.FilePathSource.MERGE_BASE: conflictify.ConflictingFile(conflictify.FilePathSource.MERGE_BASE, 100644, "7381df8a15bd65ebfec4dd57ca9748ec645866c6", pathlib.Path("image.png")),
				conflictify.FilePathSource.BASE: conflictify.ConflictingFile(conflictify.FilePathSource.BASE, 100644, "38682de80d879d6644576907223d620a1058144b", pathlib.Path("image.png")),
				conflictify.FilePathSource.HEAD: conflictify.ConflictingFile(conflictify.FilePathSource.HEAD, 100644, "eac0ec2cd3ee88ad931b3c64c8186a97108b535b", pathlib.Path("image.png")),
			},
		],
	)

def test_submodule():
	do_test(
		"submodule",
		[
			{
				conflictify.FilePathSource.MERGE_BASE: conflictify.ConflictingFile(conflictify.FilePathSource.MERGE_BASE, 160000, "d8705b294d767f8c9322d2d913005caa84210d61", pathlib.Path("plaintext")),
				conflictify.FilePathSource.BASE: conflictify.ConflictingFile(conflictify.FilePathSource.BASE, 160000, "b6138f710832b0fbcad820c9712c7e835af2105b", pathlib.Path("plaintext")),
				conflictify.FilePathSource.HEAD: conflictify.ConflictingFile(conflictify.FilePathSource.HEAD, 160000, "54986cd2bf5590eaea0681fee1e73090e94dc9bf", pathlib.Path("plaintext")),
			},
		],
	)
