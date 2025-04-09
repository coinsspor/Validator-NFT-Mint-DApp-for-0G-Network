// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ValidatorNFT is ERC721Enumerable, Ownable {
    uint256 public nextTokenId;
    uint256 public constant maxSupply = 500;

    mapping(address => bool) public hasMinted;
    mapping(address => bool) public isValidator;

    string public baseTokenURI;

    event ValidatorStatusChanged(address indexed validator, bool status);
    event Minted(address indexed validator, uint256 tokenId);

    constructor(string memory _baseTokenURI) ERC721("Validator OG NFT", "VNFT") Ownable(msg.sender) {
        baseTokenURI = _baseTokenURI;
    }

    function setValidator(address _addr, bool _status) public onlyOwner {
        isValidator[_addr] = _status;
        emit ValidatorStatusChanged(_addr, _status);
    }

    function batchSetValidators(address[] calldata addrs, bool status) public onlyOwner {
        for (uint i = 0; i < addrs.length; i++) {
            isValidator[addrs[i]] = status;
            emit ValidatorStatusChanged(addrs[i], status);
        }
    }

    function mint() public {
        require(isValidator[msg.sender], "Only validators can mint");
        require(!hasMinted[msg.sender], "Already minted");
        require(nextTokenId < maxSupply, "Max supply reached");

        _safeMint(msg.sender, nextTokenId);
        emit Minted(msg.sender, nextTokenId);
        hasMinted[msg.sender] = true;
        nextTokenId++;
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        require(ownerOf(tokenId) != address(0), "ERC721Metadata: URI query for nonexistent token");
        return baseTokenURI;
    }

    function _baseURI() internal view override returns (string memory) {
        return baseTokenURI;
    }
}
