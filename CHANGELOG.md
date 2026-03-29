## [1.8.2](https://github.com/easytocloud/sso-config-generator/compare/v1.8.1...v1.8.2) (2026-03-29)


### Bug Fixes

* rebuild cache when use_ou_structure=true but cache was built flat ([b791b14](https://github.com/easytocloud/sso-config-generator/commit/b791b14ddd012831b9617914c4667b3e437bee6e))

## [1.8.1](https://github.com/easytocloud/sso-config-generator/compare/v1.8.0...v1.8.1) (2026-03-29)


### Bug Fixes

* honour --sso-name override when sso-session section exists in config ([60928ab](https://github.com/easytocloud/sso-config-generator/commit/60928abde948e41f1ba029c765173a2857adb680))

# [1.8.0](https://github.com/easytocloud/sso-config-generator/compare/v1.7.1...v1.8.0) (2026-03-29)


### Features

* replace .generate-sso-config with .sso-config-generator.ini ([2d57e27](https://github.com/easytocloud/sso-config-generator/commit/2d57e27475d74b9455d1635c273d2bd912045b52))

## [1.7.1](https://github.com/easytocloud/sso-config-generator/compare/v1.7.0...v1.7.1) (2026-03-29)


### Bug Fixes

* drop Python <3.10 support to resolve urllib3 CVEs ([00bd52d](https://github.com/easytocloud/sso-config-generator/commit/00bd52dd7a568d4525d5077325900eddab9b1215))

# [1.7.0](https://github.com/easytocloud/sso-config-generator/compare/v1.6.1...v1.7.0) (2026-03-29)


### Features

* overhaul CLI defaults, add ini config support, and improve cache placement ([6b17497](https://github.com/easytocloud/sso-config-generator/commit/6b17497284625d32d31c17f42bd98c935e64e7b2))

## [1.6.1](https://github.com/easytocloud/sso-config-generator/compare/v1.6.0...v1.6.1) (2026-03-27)


### Bug Fixes

* properly parse ISO 8601 expiresAt in SSO token cache ([4d2112b](https://github.com/easytocloud/sso-config-generator/commit/4d2112b861e94736456a1b8a0baa1230e4903a36))

# [1.6.0](https://github.com/easytocloud/sso-config-generator/compare/v1.5.4...v1.6.0) (2026-03-27)


### Features

* add --sso-session-name option for multiple concurrent SSO sessions ([fefa537](https://github.com/easytocloud/sso-config-generator/commit/fefa537921f5a91672e9b65d33c153b987d79d9a))

## [1.5.4](https://github.com/easytocloud/sso-config-generator/compare/v1.5.3...v1.5.4) (2026-03-27)


### Bug Fixes

* search SSO tokens only in ~/.aws/sso/cache (always consistent location) ([1eb4e00](https://github.com/easytocloud/sso-config-generator/commit/1eb4e00c362d944303087ef592fa5ce207949173))

## [1.5.3](https://github.com/easytocloud/sso-config-generator/compare/v1.5.2...v1.5.3) (2026-03-27)


### Bug Fixes

* search for SSO token matching startUrl and expiration instead of most recent file ([6c5ca1f](https://github.com/easytocloud/sso-config-generator/commit/6c5ca1f6a6e2f61f5e5ce101d2ff6e8b3d051ab5))

## [1.5.2](https://github.com/easytocloud/sso-config-generator/compare/v1.5.1...v1.5.2) (2026-03-27)


### Bug Fixes

* respect AWS_CONFIG_FILE for SSO token cache directory lookup ([b84b400](https://github.com/easytocloud/sso-config-generator/commit/b84b4003ef080578dba31ed6e687b2417995a6c1))

## [1.5.1](https://github.com/easytocloud/sso-config-generator/compare/v1.5.0...v1.5.1) (2026-03-27)


### Bug Fixes

* restore SSO token handling for SSO API calls requiring explicit accessToken ([96f37d9](https://github.com/easytocloud/sso-config-generator/commit/96f37d916c49fd6ae18a6657128ab58fee30fac0))

# [1.5.0](https://github.com/easytocloud/sso-config-generator/compare/v1.4.2...v1.5.0) (2026-03-27)


### Features

* explicitly use sso-browser profile for all AWS APIs and document required IAM permissions ([6d4fd57](https://github.com/easytocloud/sso-config-generator/commit/6d4fd57b3c5f009522176fea97061102de3e3d9e))

## [1.4.2](https://github.com/easytocloud/sso-config-generator/compare/v1.4.1...v1.4.2) (2026-03-27)


### Bug Fixes

* scope OU cache per organization and expire after 7 days ([a198ee7](https://github.com/easytocloud/sso-config-generator/commit/a198ee7f72cf2647dcc17ec79b082b898372090e))

## [1.4.1](https://github.com/easytocloud/sso-config-generator/compare/v1.4.0...v1.4.1) (2025-11-14)

# [1.4.0](https://github.com/easytocloud/sso-config-generator/compare/v1.3.1...v1.4.0) (2025-11-14)


### Features

* add removal of config.needed ([e6fe0d5](https://github.com/easytocloud/sso-config-generator/commit/e6fe0d58b0f979d0889df56ab6ab22e295fae2c3))

## [1.3.1](https://github.com/easytocloud/sso-config-generator/compare/v1.3.0...v1.3.1) (2025-11-14)


### Bug Fixes

* runs with reduced permissions ([3036f03](https://github.com/easytocloud/sso-config-generator/commit/3036f03fd698cff3df35a1ab4e8987dc29a44c5b))

# [1.3.0](https://github.com/easytocloud/sso-config-generator/compare/v1.2.5...v1.3.0) (2025-09-29)


### Features

* add region parameter support ([76f724c](https://github.com/easytocloud/sso-config-generator/commit/76f724c18d13b373927beeb554e70f1a4eac32f1))

## [1.2.5](https://github.com/easytocloud/sso-config-generator/compare/v1.2.4...v1.2.5) (2025-09-29)

## [1.2.4](https://github.com/easytocloud/sso-config-generator/compare/v1.2.3...v1.2.4) (2025-03-04)

## [1.2.3](https://github.com/easytocloud/sso-config-generator/compare/v1.2.2...v1.2.3) (2025-03-04)


### Bug Fixes

* handle blanks in account_names better ([98f5748](https://github.com/easytocloud/sso-config-generator/commit/98f574877450757c8aae41809c5a97275a8559ad))

## [1.2.2](https://github.com/easytocloud/sso-config-generator/compare/v1.2.1...v1.2.2) (2025-03-04)


### Bug Fixes

* versioning to 1.3.0 ([3153a1c](https://github.com/easytocloud/sso-config-generator/commit/3153a1c492d3b2fa5e83335d7457ef5d7a38544c))

## [1.2.1](https://github.com/easytocloud/sso-config-generator/compare/v1.2.0...v1.2.1) (2025-03-04)


### Bug Fixes

* versioning ([71022e5](https://github.com/easytocloud/sso-config-generator/commit/71022e553464c3c93413ec6f2aa861bf532adee2))

# 1.2.0 (2025-03-04)

### Features

* add automatic detection of Cloud9/CloudX environments ([bc9a001](https://github.com/easytocloud/sso-config-generator/commit/bc9a001339d6be3d94886b317e65906e6c23d1bd))

# 1.0.0 (2025-03-04)


### Bug Fixes

* correct cache file handling and documentation ([0b2bfa3](https://github.com/easytocloud/sso-config-generator/commit/0b2bfa34380f753580668757db1ed1f7bccdd434))
* improved cloudX detection ([bc9a001](https://github.com/easytocloud/sso-config-generator/commit/bc9a001339d6be3d94886b317e65906e6c23d1bd))
* many small fixes and performace improvements ([f8e3eea](https://github.com/easytocloud/sso-config-generator/commit/f8e3eea9b6692c6c78b8a3fe510bea11fd1f4651))
* update GitHub workflow to correctly detect semantic release version ([6b36823](https://github.com/easytocloud/sso-config-generator/commit/6b36823638cbd005a78faf2cdb821b3bade138fc))
* update version to 0.3.0 ([c84ce86](https://github.com/easytocloud/sso-config-generator/commit/c84ce86d2d51abbb8e3414d710d4498e361f0421))
* use uv for testing ([08815ed](https://github.com/easytocloud/sso-config-generator/commit/08815ede16d283b13783fd2132160029214a6290))


### Features

* align version to 1.0.2 and add automated version updates ([5ed62ff](https://github.com/easytocloud/sso-config-generator/commit/5ed62ffd6c3e8b1e683bad574a68dcad6af87617))
* improve development setup with uv and enhance documentation ([11ed92a](https://github.com/easytocloud/sso-config-generator/commit/11ed92a4050eda864d76889d581d5fdcf92b896a))
* Initial commit with SSO config generator functionality ([cf15ef4](https://github.com/easytocloud/sso-config-generator/commit/cf15ef40c0bf51bcd069a129d95c4c3d5a473dcb))
* simplify CLI interface and improve directory handling ([51bae4b](https://github.com/easytocloud/sso-config-generator/commit/51bae4b302df270dde44c6edd8baa21c08bc4c8d))
* simplify CLI interface and improve directory handling ([bbe818a](https://github.com/easytocloud/sso-config-generator/commit/bbe818aea4a43aae7911c7f4f780fd2645cb7ddc))

# 1.0.0 (2025-02-25)


### Bug Fixes

* correct cache file handling and documentation ([0b2bfa3](https://github.com/easytocloud/sso-config-generator/commit/0b2bfa34380f753580668757db1ed1f7bccdd434))
* many small fixes and performace improvements ([f8e3eea](https://github.com/easytocloud/sso-config-generator/commit/f8e3eea9b6692c6c78b8a3fe510bea11fd1f4651))
* update GitHub workflow to correctly detect semantic release version ([6b36823](https://github.com/easytocloud/sso-config-generator/commit/6b36823638cbd005a78faf2cdb821b3bade138fc))
* update version to 0.3.0 ([c84ce86](https://github.com/easytocloud/sso-config-generator/commit/c84ce86d2d51abbb8e3414d710d4498e361f0421))
* use uv for testing ([08815ed](https://github.com/easytocloud/sso-config-generator/commit/08815ede16d283b13783fd2132160029214a6290))


### Features

* align version to 1.0.2 and add automated version updates ([5ed62ff](https://github.com/easytocloud/sso-config-generator/commit/5ed62ffd6c3e8b1e683bad574a68dcad6af87617))
* improve development setup with uv and enhance documentation ([11ed92a](https://github.com/easytocloud/sso-config-generator/commit/11ed92a4050eda864d76889d581d5fdcf92b896a))
* Initial commit with SSO config generator functionality ([cf15ef4](https://github.com/easytocloud/sso-config-generator/commit/cf15ef40c0bf51bcd069a129d95c4c3d5a473dcb))
* simplify CLI interface and improve directory handling ([51bae4b](https://github.com/easytocloud/sso-config-generator/commit/51bae4b302df270dde44c6edd8baa21c08bc4c8d))
* simplify CLI interface and improve directory handling ([bbe818a](https://github.com/easytocloud/sso-config-generator/commit/bbe818aea4a43aae7911c7f4f780fd2645cb7ddc))

## [1.1.1](https://github.com/easytocloud/sso-config-generator/compare/v1.1.0...v1.1.1) (2025-02-25)

# [1.1.0](https://github.com/easytocloud/sso-config-generator/compare/v1.0.2...v1.1.0) (2025-02-25)


### Features

* align version to 1.0.2 and add automated version updates ([70af946](https://github.com/easytocloud/sso-config-generator/commit/70af94672e75c1b3c4efd3117385f7bc1ac42bb0))

## [1.0.2](https://github.com/easytocloud/sso-config-generator/compare/v1.0.1...v1.0.2) (2025-02-25)


### Bug Fixes

* update version to 0.3.0 ([b94c064](https://github.com/easytocloud/sso-config-generator/commit/b94c064fd58056f42167d22ad15bd5ff477bafb3))

## [1.0.1](https://github.com/easytocloud/sso-config-generator/compare/v1.0.0...v1.0.1) (2025-02-25)


### Bug Fixes

* correct cache file handling and documentation ([0ddb3ca](https://github.com/easytocloud/sso-config-generator/commit/0ddb3caabbed28215b0e93e3875d3cad900a0e33))

# 1.0.0 (2025-02-25)


### Bug Fixes

* many small fixes and performace improvements ([d3e17c8](https://github.com/easytocloud/sso-config-generator/commit/d3e17c84e9cd5f5a3978ac15319ba9538d2d7935))
* update GitHub workflow to correctly detect semantic release version ([8d918a6](https://github.com/easytocloud/sso-config-generator/commit/8d918a68b52c0c6397ce96f2b287ba165ceb4058))
* use uv for testing ([704b651](https://github.com/easytocloud/sso-config-generator/commit/704b65151c801068561c7d3baa06ece408829d5a))


### Features

* improve development setup with uv and enhance documentation ([11ed92a](https://github.com/easytocloud/sso-config-generator/commit/11ed92a4050eda864d76889d581d5fdcf92b896a))
* Initial commit with SSO config generator functionality ([cf15ef4](https://github.com/easytocloud/sso-config-generator/commit/cf15ef40c0bf51bcd069a129d95c4c3d5a473dcb))
* simplify CLI interface and improve directory handling ([08dd24f](https://github.com/easytocloud/sso-config-generator/commit/08dd24f08a06a1e4d5ebbba54a4f9c839d2bd03d))
* simplify CLI interface and improve directory handling ([e56cb04](https://github.com/easytocloud/sso-config-generator/commit/e56cb04cbd4d9d7dd5194af89a1b8743933702e6))

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
