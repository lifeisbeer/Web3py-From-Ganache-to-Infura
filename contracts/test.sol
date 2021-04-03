// SPDX-License-Identifier: GPLv3

pragma solidity ^0.8.1;
pragma abicoder v2;
pragma experimental SMTChecker;

contract test {
  uint public num;

  // inform participants about current state
  event change(uint number);

  function set(uint _num) external {
    num = _num;
    emit change(num);
  }
}
