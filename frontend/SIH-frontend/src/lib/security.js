// Security utilities and minimal blockchain logic matching original site behavior
import CryptoJS from 'crypto-js';

export const SecuritySystem = {
  encryptionKey: CryptoJS.lib.WordArray.random(256 / 8),
  iv: CryptoJS.lib.WordArray.random(128 / 8),
  encrypt(data) {
    return CryptoJS.AES.encrypt(
      JSON.stringify(data),
      this.encryptionKey,
      { iv: this.iv, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 }
    ).toString();
  },
  decrypt(encrypted) {
    const bytes = CryptoJS.AES.decrypt(
      encrypted,
      this.encryptionKey,
      { iv: this.iv, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 }
    );
    return JSON.parse(bytes.toString(CryptoJS.enc.Utf8));
  }
};

export const blockchain = {
  chain: [],
  pendingTransactions: [],
  createBlock(previousHash = '0') {
    const block = {
      timestamp: Date.now(),
      transactions: this.pendingTransactions,
      previousHash,
      hash: '',
      nonce: 0
    };
    block.hash = this.calculateHash(block);
    this.chain.push(block);
    this.pendingTransactions = [];
    return block;
  },
  calculateHash(block) {
    return CryptoJS.SHA256(
      block.timestamp + JSON.stringify(block.transactions) + block.previousHash + block.nonce
    ).toString();
  },
  addTransaction(tx) {
    this.pendingTransactions.push({ ...tx, timestamp: Date.now() });
    if (this.pendingTransactions.length >= 3) {
      this.createBlock(this.chain.length ? this.chain[this.chain.length - 1].hash : '0');
    }
  }
};

// initialize genesis block
blockchain.createBlock('0');


