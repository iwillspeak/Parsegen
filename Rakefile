require 'rake/clean'

desc "Default task"
task :default => ['build']

DOC_SRCS = FileList['docs/*.ronn']
DOCS = DOC_SRCS.ext("") + DOC_SRCS.ext("html")

DOCS.each { |f| CLEAN << f }
CLOBBER << 'build'

desc "Build the package"
file 'build' => DOCS do
  puts "building package"
  `python setup.py build`
end

desc "Push the package to PyPi"
task :push do
  `python setup.py sdist upload`
end

# Rule to convert ronn formatted manpages to compiled ones
rule '.html' => ['.ronn'] do |t|
  `ronn --style=dark,toc --html #{t.source}`
end

# Rule to convert ronn formatted manpages to compiled ones
rule /\.[0-9]$/ => [ proc { |t| t + '.ronn' } ] do |t|
  `ronn --roff #{t.source}`
end

# Build the docs : rake docs
desc "Build the manpages"
task :docs => DOCS

task :test do
  sh %{nosetests}
end
