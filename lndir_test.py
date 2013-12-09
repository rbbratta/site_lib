#  Copyright(c) 2013 Intel Corporation.
#
#  This program is free software; you can redistribute it and/or modify it
#  under the terms and conditions of the GNU General Public License,
#  version 2, as published by the Free Software Foundation.
#
#  This program is distributed in the hope it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin St - Fifth Floor, Boston, MA 02110-1301 USA.
#
#  The full GNU General Public License is included in this distribution in
#  the file called "COPYING".


from subprocess import call

import lndir


def make_it(tmpdir):
    t = tmpdir.mkdir("sub")
    t.chdir()
    a_d = t.mkdir('a')
    a_d.join('1').write('1')
    a_d.join('2').write('2')
    a_d.join('3').write('3')
    a_d.mkdir('A')
    b_d = t.mkdir('b')
    b_d.join('1').write('1')
    b_d.join('2').mksymlinkto(a_d.join('2'), absolute=0)
    b_d.join('3').write('3')
    c_d = t.mkdir('c')
    c_d.join('1').write('1')
    c_d.join('2').write('2')
    c_d.join('3').write('3')
    c_d.join('A').mksymlinkto(a_d.join('A'), absolute=0)
    t.join('d').mksymlinkto('c')
    e_d = t.mkdir('e')
    e_d.join('1').write('1')
    e_d.join('2').write('2')
    e_d.join('3').mksymlinkto(a_d.join('3'), absolute=1)
    e_d.join('A').mksymlinkto(a_d.join('A'), absolute=1)
    return t


def test_create_abs(tmpdir):
    src_dir = make_it(tmpdir)
    tmpdir.chdir()
    dst = tmpdir.mkdir("dest")
    lndir.lndir(str(src_dir), str(dst))
    call(["tree", "-Ffin"])
    call(["diff", "--brief", "-r", str(src_dir), str(dst)])

# ./dest/
# ./dest/a/
# ./dest/a/1 -> /tmp/pytest-60/test_create_abs0/sub/a/1
# ./dest/a/2 -> /tmp/pytest-60/test_create_abs0/sub/a/2
# ./dest/a/3 -> /tmp/pytest-60/test_create_abs0/sub/a/3
# ./dest/a/A/
# ./dest/b/
# ./dest/b/1 -> /tmp/pytest-60/test_create_abs0/sub/b/1
# ./dest/b/2 -> ../a/2
# ./dest/b/3 -> /tmp/pytest-60/test_create_abs0/sub/b/3
# ./dest/c/
# ./dest/c/1 -> /tmp/pytest-60/test_create_abs0/sub/c/1
# ./dest/c/2 -> /tmp/pytest-60/test_create_abs0/sub/c/2
# ./dest/c/3 -> /tmp/pytest-60/test_create_abs0/sub/c/3
# ./dest/c/A -> ../a/A/
# ./dest/d -> c/
# ./dest/e/
# ./dest/e/1 -> /tmp/pytest-60/test_create_abs0/sub/e/1
# ./dest/e/2 -> /tmp/pytest-60/test_create_abs0/sub/e/2
# ./dest/e/3 -> /tmp/pytest-60/test_create_abs0/sub/a/3
# ./dest/e/A -> /tmp/pytest-60/test_create_abs0/sub/a/A/
# ./sub/
# ./sub/a/
# ./sub/a/1
# ./sub/a/2
# ./sub/a/3
# ./sub/a/A/
# ./sub/b/
# ./sub/b/1
# ./sub/b/2 -> ../a/2
# ./sub/b/3
# ./sub/c/
# ./sub/c/1
# ./sub/c/2
# ./sub/c/3
# ./sub/c/A -> ../a/A/
# ./sub/d -> c/
# ./sub/e/
# ./sub/e/1
# ./sub/e/2
# ./sub/e/3 -> /tmp/pytest-60/test_create_abs0/sub/a/3
# ./sub/e/A -> /tmp/pytest-60/test_create_abs0/sub/a/A/


def test_create_rel(tmpdir):
    src_dir = make_it(tmpdir)
    tmpdir.chdir()
    dst = tmpdir.mkdir("dest")
    lndir.lndir("../sub", str(dst))
    call(["tree", "-Ffin"])
    call(["diff", "--brief", "-r", str(src_dir), str(dst)])

# ./dest/
# ./dest/a/
# ./dest/a/1 -> ../../sub/a/1
# ./dest/a/2 -> ../../sub/a/2
# ./dest/a/3 -> ../../sub/a/3
# ./dest/a/A/
# ./dest/b/
# ./dest/b/1 -> ../../sub/b/1
# ./dest/b/2 -> ../a/2
# ./dest/b/3 -> ../../sub/b/3
# ./dest/c/
# ./dest/c/1 -> ../../sub/c/1
# ./dest/c/2 -> ../../sub/c/2
# ./dest/c/3 -> ../../sub/c/3
# ./dest/c/A -> ../a/A/
# ./dest/d -> c/
# ./dest/e/
# ./dest/e/1 -> ../../sub/e/1
# ./dest/e/2 -> ../../sub/e/2
# ./dest/e/3 -> /tmp/pytest-60/test_create_rel0/sub/a/3
# ./dest/e/A -> /tmp/pytest-60/test_create_rel0/sub/a/A/
# ./sub/
# ./sub/a/
# ./sub/a/1
# ./sub/a/2
# ./sub/a/3
# ./sub/a/A/
# ./sub/b/
# ./sub/b/1
# ./sub/b/2 -> ../a/2
# ./sub/b/3
# ./sub/c/
# ./sub/c/1
# ./sub/c/2
# ./sub/c/3
# ./sub/c/A -> ../a/A/
# ./sub/d -> c/
# ./sub/e/
# ./sub/e/1
# ./sub/e/2
# ./sub/e/3 -> /tmp/pytest-60/test_create_rel0/sub/a/3
# ./sub/e/A -> /tmp/pytest-60/test_create_rel0/sub/a/A/
