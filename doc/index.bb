=?= [center]Lutin Build system[/center] =?=
___________________________________________

===What is Lutin, and how can I use it?===

Lutin is an application/library builder, it is designed to concurence CMake, Makefile, Ant, graddle ...

Lutin is deveopped in Python 2.x and 3.x to permit many user to play with it.

Python permit to Lutin to be used in many environement in a fast way.

Lutin support can compile every thing you want, just add a builder that you need (not in the common way). Basicly Lutin support languages:
:** C (ainsi/89/99) ==> .o;
:** C++ (98/99/03/11/14/...) ==> .o;
:** .S (assembleur) ==> .o;
:** .java ==> .class;
:** .class ==> jar;
:** .o ==> .a;
:** .o ==> .so;
:** .o/.a ==> binary.

Some packege can be generate for some platform:
:** debian package;
:** windows application zip;
:** MacOs application .app;
:** iOs package;
:** Android Package .apk.

Compilation is availlable for:
:** gcc/g++;
:** clang/clang++.

Manage [b]workspace build[/b] (in oposition of CMake/make/...)


=== Install: ===

Requirements: ``Python >= 2.7`` and ``pip``

==== Install lutin: ===
Just run:
[code style=bash]
	pip install lutin
[/code]

==== Install pip ====
Install pip on debian/ubuntu:
[code style=bash]
	sudo apt-get install pip
[/code]

Install pip on ARCH-linux:
[code style=bash]
	sudo pacman -S pip
[/code]

Install pip on MacOs:
[code style=bash]
	sudo easy_install pip
[/code]

==== Install from sources ====

[code style=bash]
	git clone http://github.com/HeeroYui/lutin.git
	cd lutin
	sudo ./setup.py install
[/code]

=== License (APACHE v2.0) ===

Copyright lutin Edouard DUPIN

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


=== History: ===

I work with some builder, Every one have theire own adventages, and their problems.
The main point I see, is that the polimorphisme of the worktree is really hard.
The second point is the generation on different platforms is hard too.

Some other problem example:
:** Makefile is too slow on windows mingw;
:** Cmake does not create end point package;
:** none is really simple to write.

Then I create a simple interface that manage all I need. and written in python to permit to be faster on every platform.

[tutorial[000_Build | Tutorials]]
