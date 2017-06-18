import argparse, os, termcolor, time

from hamplify.config import *
from hamplify.parsers.parser import Parser

arg_parser = argparse.ArgumentParser(description="Convert HAML files to HTML.")
arg_parser.add_argument("src", metavar="source", help="A path to a single file or dir containing .haml files")
arg_parser.add_argument("dst", metavar="dest", nargs="?", help="A path to where the "
  "converted file(s) should go (defaults to src directory)")
arg_parser.add_argument("-e", "--ext", metavar="extension", default=["haml"], nargs="+", 
  help="The extensions of the haml files to look for (defaults to 'haml')")
arg_parser.add_argument("-o", "--out", metavar="extension", default="html", nargs="?", 
  help="The extension to save the converted files as (defaults to 'html')")
arg_parser.add_argument("-v", "--verbose", action="store_true", 
  help="Verbose mode. Prints out file paths as files are being converted")
arg_parser.add_argument("--django", action="store_true", 
  help="Parses the file(s) with Django syntax and tag names")
arg_parser.add_argument("--jinja", action="store_true", 
  help="(default) Parses the file(s) with Jinja syntax and tag names")
arg_parser.add_argument("-w", "--watch", action="store_true",
  help="Watches the src directory for changes. Source path must refer to a directory if using this flag")

class HamplifyCompiler():
  def __init__(self, args):
    self.args = args
    self.parser = None

  def run(self):
    self._run_checks()

    args = self.args

    print("Working...")
    earlier = time.time()

    # Converting just a single file
    if os.path.isfile(args.src):
      self._convert_file()

      if args.verbose:
        print()

      print("Finished converting in %d ms." % ((time.time() - earlier) * 1000))
    else:
      count, converted = self._convert_dir()

      if args.verbose and count > 0:
        print()

      print(termcolor.colored("Finished converting %d file(s) in %d ms." 
        % (converted, (time.time() - earlier) * 1000), "green"))

      if count != converted:
        print(termcolor.colored("FAILED: %d file(s) failed to compile." % (count - converted), "red"))

  def _run_checks(self):
    """ Runs some checks on the arguments and normalizes paths
    """

    args = self.args

    # If using watch mode, make sure that `src` is a directory
    if args.watch and not os.path.isdir(args.src):
      print("Source path must point to a directory when using watch mode (-w, --watch flag).")
      exit(1)

    if not os.path.exists(args.src):
      print("Source path or file does not exist: %s" % args.src)
      exit(1)

    if args.django:
      self.parser = Parser({"engine": ENGINE_DJANGO})
    else:
      self.parser = Parser({"engine": ENGINE_JINJA})

    # Output dir defaults to the source
    if not args.dst:
      if os.path.isfile(args.src):
        args.dst = os.path.dirname(args.src)
      else:
        args.dst = args.src

    # Make sure all extensions start with a period
    for i in range(len(args.ext)):
      if not args.ext[i].startswith("."):
        args.ext[i] = "." + args.ext[i]

    # Make sure the output file extention starts with a period
    if not args.out.startswith("."):
      args.out = "." + args.out

    # Normalize paths to be the full path
    args.src = os.path.realpath(args.src)
    args.dst = os.path.realpath(args.dst)

  def _create_out_dir(self, path):
    try:
      os.makedirs(path)
    except OSError:
      pass

  def _convert_dir(self):
    """ Recursively walks a path, converting every haml file it finds, then returns how
    many files were converted
    """

    args = self.args
    file_count = 0
    converted = 0
    
    for path, dirs, files in os.walk(args.src):
      out_path = os.path.join(args.dst, os.path.relpath(path, args.src))

      # If the dst folder is inside the src folder, skip over it
      if path.startswith(args.dst) and args.dst != args.src:
        continue

      self._create_out_dir(out_path)
      
      for f in files:
        # Check if the file extension matches
        for ext in args.ext:
          if f.endswith(ext):
            file_count += 1

            # Remove the extension so we can replace it with the output extension
            if self._write_file(os.path.join(path, f), os.path.join(out_path, f[:-len(ext)]) + args.out):
              converted += 1
              break

    return file_count, converted

  def _convert_file(self):
    """ Converts a single file
    """

    args = self.args

    self._create_out_dir(os.path.dirname(args.dst))
    file_name = os.path.basename(args.src).split(".")[0] + args.out
    self._write_file(args.src, os.path.join(args.dst, file_name))

  def _write_file(self, in_file, out_file):
    """ Converts a file and saves it to the destination folder
    """

    args = self.args

    if args.verbose:
      print()
      print("Input file:   %s" % os.path.relpath(in_file))
      print("Output file:  %s" % os.path.relpath(out_file))

    earlier = time.time()
    success = True

    with open(in_file, "r") as fin:
      with open(out_file, "w") as fout:
        buffer = fin.read()

        try:
          fout.write(self.parser.parse(buffer).render())
        except ParseError as pe:
          pe.file_path = os.path.relpath(in_file)
          print(termcolor.colored(pe, "red"))
          success = False

    if args.verbose:
      if success:
        print("Conversion took %.3f ms" % ((time.time() - earlier) * 1000))
      else:
        print("Conversion took %.3f ms %s" % ((time.time() - earlier) * 1000, termcolor.colored("(FAILED)", "red")))

    return success

def main():
  HamplifyCompiler(arg_parser.parse_args()).run()