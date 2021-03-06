#!/usr/bin/expect -f

#Usage sshsudologin.expect <host> <ssh user> <ssh password>

set timeout 60

spawn ssh [lindex $argv 1]@[lindex $argv 0]

expect "yes/no" {
        send "yes\r"
	expect "*?assword" { send "[lindex $argv 2]\r" }
	} "*?assword" { send "[lindex $argv 2]\r" }

interact
