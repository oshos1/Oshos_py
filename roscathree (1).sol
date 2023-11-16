// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AdvancedROSCA {
    struct Member {
        address payable addr;
        bool hasBenefitted;
        bool isActive;
        bool hasContributed;
    }
    
    Member[] public members;
    uint256 public contributionAmount;
    uint256 public penaltyPercentage = 10; // penalty is 10% of the contributionAmount
    uint256 public totalContributions;
    uint256 public currentRound = 0;
    uint256 public roscaStartTime;
    uint256 public savingsMonths = 0;
    
    mapping(address => uint256) public balances;

    event Joined(address member);
    event ContributionMade(address contributor);
    event BeneficiaryPaid(address beneficiary, uint256 amount);
    event NewRoundStarted(uint256 round);
    event ROSCAStarted();
    event PenaltyApplied(address member, uint256 penaltyAmount);

    modifier onlyMember() {
        bool isMember = false;
        for (uint i = 0; i < members.length; i++) {
            if (members[i].addr == msg.sender && members[i].isActive) {
                isMember = true;
                break;
            }
        }
        require(isMember, "Only a member can call this");
        _;
    }

    constructor(uint256 _contributionAmount, uint256 _savingsMonths) {
        require(_contributionAmount > 0, "Contribution amount should be greater than 0");
        contributionAmount = _contributionAmount;
        savingsMonths = _savingsMonths;
        roscaStartTime = block.timestamp + 30 days;
    }

    function join() external {
        require(members.length < 12, "Maximum number of members reached");
        for (uint i = 0; i < members.length; i++) {
            require(members[i].addr != msg.sender, "Address already joined");
        }
        members.push(Member({ addr: payable(msg.sender), hasBenefitted: false, isActive: true, hasContributed: false }));
        emit Joined(msg.sender);
        
        if (members.length == 12) {
            startROSCA();
        }
    }
    
    function startROSCA() internal {
        require(roscaStartTime > block.timestamp, "ROSCA start time exceeded");
        require(members.length >= 3, "Minimum number of members not met");
        emit ROSCAStarted();
    }

    function contribute() external payable onlyMember {
        require(block.timestamp >= roscaStartTime, "ROSCA has not started");
        require(msg.value == contributionAmount, "Must contribute the required amount");
        for (uint i = 0; i < members.length; i++) {
            if (members[i].addr == msg.sender) {
                members[i].hasContributed = true;
                break;
            }
        }
        balances[msg.sender] += msg.value;
        totalContributions += msg.value;
        emit ContributionMade(msg.sender);
        
        if (totalContributions == contributionAmount * members.length) {
            applyPenalties();
            selectBeneficiaryAndPay();
            currentRound++;
            totalContributions = 0;
            resetContributions();
            emit NewRoundStarted(currentRound);
        }
    }

    function applyPenalties() internal {
        uint256 penaltyAmount = (contributionAmount * penaltyPercentage) / 100;
        for (uint i = 0; i < members.length; i++) {
            if (!members[i].hasContributed && members[i].isActive) {
                balances[members[i].addr] = (balances[members[i].addr] >= penaltyAmount) ? (balances[members[i].addr] - penaltyAmount) : 0;
                emit PenaltyApplied(members[i].addr, penaltyAmount);
            }
        }
    }

    function resetContributions() internal {
        for (uint i = 0; i < members.length; i++) {
            members[i].hasContributed = false;
        }
    }

    function selectBeneficiaryAndPay() internal {
        require(totalContributions == contributionAmount * members.length, "Not enough contributions for this round");
        
        uint index;
        bool beneficiarySelected = false;
        uint256 randomSeed = uint256(keccak256(abi.encodePacked(block.timestamp, block.difficulty, msg.sender)));
        while (!beneficiarySelected) {
            index = randomSeed % members.length;
            if (!members[index].hasBenefitted && members[index].isActive) {
                beneficiarySelected = true;
                members[index].addr.transfer(totalContributions);
                members[index].hasBenefitted = true;
                emit BeneficiaryPaid(members[index].addr, totalContributions);
            }
            randomSeed++;
        }
    }

    function leave() external onlyMember {
        for (uint i = 0; i < members.length; i++) {
            if (members[i].addr == msg.sender) {
                members[i].isActive = false;
                payable(msg.sender).transfer(balances[msg.sender]);
                balances[msg.sender] = 0;
                break;
            }
        }
    }
}
