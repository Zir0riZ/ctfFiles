#!/usr/bin/env python3
import sys
import os
import binwalk
import shlex
import subprocess as sp

def dump_file(file, offset, size, outfile):
	cmd = "dd if={} of={} bs=1 skip={}".format(file, outfile, offset, size)
	if size is not None:
		cmd += " count={}".format(size)
	s = sp.run(shlex.split(cmd))

if __name__ == '__main__':

	if len(sys.argv) != 3:
		print("./{} <input_file> <output_dir>".format(sys.argv[0]), file=sys.stderr)
		sys.exit()
	FILE = sys.argv[1]
	OUTDIR = sys.argv[2]

	if not os.path.exists(OUTDIR):
		os.mkdir(OUTDIR)

	results = binwalk.scan(FILE, signature=True, quiet=True)[0]
	offsets = [r.offset for r in results.results]

	for i, off in enumerate(offsets):
		size = None
		if i < len(offsets)-1:
			size = offsets[i+1] - off
		dump_file(FILE, off, size, os.path.join(OUTDIR, "file{}".format(i)))
