/*
 * Copyright (c) 2018 ARM Limited. All rights reserved.
 * SPDX-License-Identifier: Apache-2.0
 * Licensed under the Apache License, Version 2.0 (the License); you may
 * not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an AS IS BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#ifndef __MBED_CLOUD_DEV_CREDENTIALS_H__
#define __MBED_CLOUD_DEV_CREDENTIALS_H__

#include <inttypes.h>

const char MBED_CLOUD_DEV_BOOTSTRAP_ENDPOINT_NAME[] = "016d3a6850395e26cf38992c03c00000";
const char MBED_CLOUD_DEV_ACCOUNT_ID[] = "016b4168981e32d9c8c3f8a300000000";
const char MBED_CLOUD_DEV_BOOTSTRAP_SERVER_URI[] = "coaps://coap-systemtest.dev.mbed.com:5684?aid=016b4168981e32d9c8c3f8a300000000";

const uint8_t MBED_CLOUD_DEV_BOOTSTRAP_DEVICE_CERTIFICATE[] = 
{ 0x30, 0x82, 0x02, 0x85, 0x30, 0x82, 0x02, 0x2a,
 0xa0, 0x03, 0x02, 0x01, 0x02, 0x02, 0x11, 0x00,
 0xc9, 0x4e, 0x75, 0xd1, 0xe2, 0xab, 0x49, 0x44,
 0x97, 0xa1, 0x66, 0x9d, 0x10, 0xeb, 0xa9, 0x0f,
 0x30, 0x0a, 0x06, 0x08, 0x2a, 0x86, 0x48, 0xce,
 0x3d, 0x04, 0x03, 0x02, 0x30, 0x81, 0xa2, 0x31,
 0x0b, 0x30, 0x09, 0x06, 0x03, 0x55, 0x04, 0x06,
 0x13, 0x02, 0x47, 0x42, 0x31, 0x17, 0x30, 0x15,
 0x06, 0x03, 0x55, 0x04, 0x08, 0x0c, 0x0e, 0x43,
 0x61, 0x6d, 0x62, 0x72, 0x69, 0x64, 0x67, 0x65,
 0x73, 0x68, 0x69, 0x72, 0x65, 0x31, 0x12, 0x30,
 0x10, 0x06, 0x03, 0x55, 0x04, 0x07, 0x0c, 0x09,
 0x43, 0x61, 0x6d, 0x62, 0x72, 0x69, 0x64, 0x67,
 0x65, 0x31, 0x10, 0x30, 0x0e, 0x06, 0x03, 0x55,
 0x04, 0x0a, 0x0c, 0x07, 0x41, 0x52, 0x4d, 0x20,
 0x4c, 0x74, 0x64, 0x31, 0x29, 0x30, 0x27, 0x06,
 0x03, 0x55, 0x04, 0x0b, 0x0c, 0x20, 0x30, 0x31,
 0x36, 0x62, 0x34, 0x31, 0x36, 0x38, 0x39, 0x38,
 0x31, 0x65, 0x33, 0x32, 0x64, 0x39, 0x63, 0x38,
 0x63, 0x33, 0x66, 0x38, 0x61, 0x33, 0x30, 0x30,
 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x31, 0x29,
 0x30, 0x27, 0x06, 0x03, 0x55, 0x04, 0x03, 0x0c,
 0x20, 0x30, 0x31, 0x36, 0x64, 0x33, 0x61, 0x36,
 0x38, 0x35, 0x30, 0x33, 0x39, 0x35, 0x65, 0x32,
 0x36, 0x63, 0x66, 0x33, 0x38, 0x39, 0x39, 0x32,
 0x63, 0x30, 0x33, 0x63, 0x30, 0x30, 0x30, 0x30,
 0x30, 0x30, 0x1e, 0x17, 0x0d, 0x31, 0x39, 0x30,
 0x39, 0x31, 0x36, 0x31, 0x34, 0x30, 0x39, 0x33,
 0x37, 0x5a, 0x17, 0x0d, 0x32, 0x39, 0x30, 0x39,
 0x31, 0x36, 0x31, 0x34, 0x30, 0x39, 0x33, 0x37,
 0x5a, 0x30, 0x81, 0xa2, 0x31, 0x0b, 0x30, 0x09,
 0x06, 0x03, 0x55, 0x04, 0x06, 0x13, 0x02, 0x47,
 0x42, 0x31, 0x17, 0x30, 0x15, 0x06, 0x03, 0x55,
 0x04, 0x08, 0x0c, 0x0e, 0x43, 0x61, 0x6d, 0x62,
 0x72, 0x69, 0x64, 0x67, 0x65, 0x73, 0x68, 0x69,
 0x72, 0x65, 0x31, 0x12, 0x30, 0x10, 0x06, 0x03,
 0x55, 0x04, 0x07, 0x0c, 0x09, 0x43, 0x61, 0x6d,
 0x62, 0x72, 0x69, 0x64, 0x67, 0x65, 0x31, 0x10,
 0x30, 0x0e, 0x06, 0x03, 0x55, 0x04, 0x0a, 0x0c,
 0x07, 0x41, 0x52, 0x4d, 0x20, 0x4c, 0x74, 0x64,
 0x31, 0x29, 0x30, 0x27, 0x06, 0x03, 0x55, 0x04,
 0x0b, 0x0c, 0x20, 0x30, 0x31, 0x36, 0x62, 0x34,
 0x31, 0x36, 0x38, 0x39, 0x38, 0x31, 0x65, 0x33,
 0x32, 0x64, 0x39, 0x63, 0x38, 0x63, 0x33, 0x66,
 0x38, 0x61, 0x33, 0x30, 0x30, 0x30, 0x30, 0x30,
 0x30, 0x30, 0x30, 0x31, 0x29, 0x30, 0x27, 0x06,
 0x03, 0x55, 0x04, 0x03, 0x0c, 0x20, 0x30, 0x31,
 0x36, 0x64, 0x33, 0x61, 0x36, 0x38, 0x35, 0x30,
 0x33, 0x39, 0x35, 0x65, 0x32, 0x36, 0x63, 0x66,
 0x33, 0x38, 0x39, 0x39, 0x32, 0x63, 0x30, 0x33,
 0x63, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x59,
 0x30, 0x13, 0x06, 0x07, 0x2a, 0x86, 0x48, 0xce,
 0x3d, 0x02, 0x01, 0x06, 0x08, 0x2a, 0x86, 0x48,
 0xce, 0x3d, 0x03, 0x01, 0x07, 0x03, 0x42, 0x00,
 0x04, 0xd5, 0xbf, 0x56, 0x36, 0x59, 0x69, 0x71,
 0x41, 0x3c, 0x73, 0xe0, 0xad, 0x0f, 0x3b, 0x8c,
 0xd8, 0xa2, 0x24, 0xb1, 0x27, 0xfd, 0xf1, 0x9d,
 0xb9, 0x78, 0x7b, 0x38, 0x09, 0x25, 0x42, 0x3f,
 0xaa, 0x3f, 0xc3, 0x2c, 0x4c, 0xbe, 0x27, 0x27,
 0xfb, 0xd8, 0x3d, 0x94, 0x2e, 0x32, 0x7c, 0x9d,
 0xd7, 0x51, 0x0b, 0x4a, 0xaf, 0x8e, 0x25, 0xc4,
 0x5e, 0x5c, 0x1b, 0x73, 0x87, 0x1e, 0x88, 0x11,
 0xa3, 0xa3, 0x3f, 0x30, 0x3d, 0x30, 0x12, 0x06,
 0x09, 0x2b, 0x06, 0x01, 0x04, 0x01, 0xa0, 0x20,
 0x81, 0x49, 0x04, 0x05, 0x02, 0x03, 0x40, 0x00,
 0x91, 0x30, 0x12, 0x06, 0x03, 0x55, 0x1d, 0x13,
 0x01, 0x01, 0xff, 0x04, 0x08, 0x30, 0x06, 0x01,
 0x01, 0xff, 0x02, 0x01, 0x00, 0x30, 0x13, 0x06,
 0x03, 0x55, 0x1d, 0x25, 0x04, 0x0c, 0x30, 0x0a,
 0x06, 0x08, 0x2b, 0x06, 0x01, 0x05, 0x05, 0x07,
 0x03, 0x02, 0x30, 0x0a, 0x06, 0x08, 0x2a, 0x86,
 0x48, 0xce, 0x3d, 0x04, 0x03, 0x02, 0x03, 0x49,
 0x00, 0x30, 0x46, 0x02, 0x21, 0x00, 0xe3, 0x1e,
 0xe2, 0x1a, 0xa3, 0x71, 0xf3, 0xe4, 0xff, 0x93,
 0x09, 0x94, 0xa9, 0xbf, 0x44, 0x28, 0xc0, 0x5b,
 0x5d, 0xf8, 0x23, 0xc0, 0xf6, 0x18, 0x1a, 0x08,
 0xf5, 0xbb, 0x61, 0xe1, 0xb7, 0xd0, 0x02, 0x21,
 0x00, 0xfd, 0x3e, 0xc8, 0x28, 0x93, 0xc9, 0x84,
 0x91, 0xfa, 0xda, 0xf6, 0x05, 0x60, 0x6d, 0x2f,
 0x2a, 0x92, 0xa2, 0x8d, 0x76, 0xde, 0xcd, 0xe7,
 0xc0, 0xd9, 0xb4, 0x5b, 0xd3, 0x06, 0xda, 0x38,
 0xe1 };

const uint8_t MBED_CLOUD_DEV_BOOTSTRAP_SERVER_ROOT_CA_CERTIFICATE[] = 
{ 0x30, 0x82, 0x02, 0x32, 0x30, 0x82, 0x01, 0xd9,
 0xa0, 0x03, 0x02, 0x01, 0x02, 0x02, 0x10, 0x45,
 0x5e, 0x28, 0x41, 0x2b, 0xca, 0xf1, 0xb1, 0x4e,
 0xea, 0xad, 0x06, 0x25, 0x6a, 0xd8, 0x4a, 0x30,
 0x0a, 0x06, 0x08, 0x2a, 0x86, 0x48, 0xce, 0x3d,
 0x04, 0x03, 0x02, 0x30, 0x71, 0x31, 0x0b, 0x30,
 0x09, 0x06, 0x03, 0x55, 0x04, 0x06, 0x13, 0x02,
 0x47, 0x42, 0x31, 0x17, 0x30, 0x15, 0x06, 0x03,
 0x55, 0x04, 0x08, 0x13, 0x0e, 0x43, 0x61, 0x6d,
 0x62, 0x72, 0x69, 0x64, 0x67, 0x65, 0x73, 0x68,
 0x69, 0x72, 0x65, 0x31, 0x12, 0x30, 0x10, 0x06,
 0x03, 0x55, 0x04, 0x07, 0x13, 0x09, 0x43, 0x61,
 0x6d, 0x62, 0x72, 0x69, 0x64, 0x67, 0x65, 0x31,
 0x10, 0x30, 0x0e, 0x06, 0x03, 0x55, 0x04, 0x0a,
 0x13, 0x07, 0x41, 0x52, 0x4d, 0x20, 0x4c, 0x74,
 0x64, 0x31, 0x23, 0x30, 0x21, 0x06, 0x03, 0x55,
 0x04, 0x03, 0x13, 0x1a, 0x41, 0x52, 0x4d, 0x20,
 0x4f, 0x66, 0x66, 0x69, 0x63, 0x69, 0x61, 0x6c,
 0x53, 0x20, 0x42, 0x6f, 0x6f, 0x74, 0x73, 0x74,
 0x72, 0x61, 0x70, 0x20, 0x43, 0x41, 0x30, 0x20,
 0x17, 0x0d, 0x31, 0x37, 0x30, 0x33, 0x32, 0x30,
 0x31, 0x35, 0x31, 0x31, 0x33, 0x33, 0x5a, 0x18,
 0x0f, 0x32, 0x30, 0x35, 0x32, 0x30, 0x33, 0x32,
 0x30, 0x31, 0x35, 0x32, 0x31, 0x33, 0x33, 0x5a,
 0x30, 0x71, 0x31, 0x0b, 0x30, 0x09, 0x06, 0x03,
 0x55, 0x04, 0x06, 0x13, 0x02, 0x47, 0x42, 0x31,
 0x17, 0x30, 0x15, 0x06, 0x03, 0x55, 0x04, 0x08,
 0x13, 0x0e, 0x43, 0x61, 0x6d, 0x62, 0x72, 0x69,
 0x64, 0x67, 0x65, 0x73, 0x68, 0x69, 0x72, 0x65,
 0x31, 0x12, 0x30, 0x10, 0x06, 0x03, 0x55, 0x04,
 0x07, 0x13, 0x09, 0x43, 0x61, 0x6d, 0x62, 0x72,
 0x69, 0x64, 0x67, 0x65, 0x31, 0x10, 0x30, 0x0e,
 0x06, 0x03, 0x55, 0x04, 0x0a, 0x13, 0x07, 0x41,
 0x52, 0x4d, 0x20, 0x4c, 0x74, 0x64, 0x31, 0x23,
 0x30, 0x21, 0x06, 0x03, 0x55, 0x04, 0x03, 0x13,
 0x1a, 0x41, 0x52, 0x4d, 0x20, 0x4f, 0x66, 0x66,
 0x69, 0x63, 0x69, 0x61, 0x6c, 0x53, 0x20, 0x42,
 0x6f, 0x6f, 0x74, 0x73, 0x74, 0x72, 0x61, 0x70,
 0x20, 0x43, 0x41, 0x30, 0x59, 0x30, 0x13, 0x06,
 0x07, 0x2a, 0x86, 0x48, 0xce, 0x3d, 0x02, 0x01,
 0x06, 0x08, 0x2a, 0x86, 0x48, 0xce, 0x3d, 0x03,
 0x01, 0x07, 0x03, 0x42, 0x00, 0x04, 0xf7, 0xdc,
 0x05, 0x70, 0x4f, 0x1b, 0x9d, 0xa8, 0x66, 0x52,
 0xf0, 0xb4, 0x99, 0x05, 0xe3, 0x89, 0x73, 0x08,
 0x4e, 0x23, 0x67, 0xdb, 0x6b, 0xac, 0x5a, 0xbe,
 0xab, 0xb0, 0x06, 0x49, 0xff, 0xd6, 0xc5, 0xd0,
 0x82, 0xbd, 0x45, 0xd5, 0x1b, 0xc2, 0x2f, 0x39,
 0x02, 0x3c, 0xf2, 0xa5, 0x42, 0x78, 0xf7, 0x55,
 0x9e, 0x9f, 0xdb, 0x3b, 0x77, 0xba, 0x0e, 0xa1,
 0x9f, 0x93, 0xcc, 0x73, 0x97, 0x99, 0xa3, 0x51,
 0x30, 0x4f, 0x30, 0x0b, 0x06, 0x03, 0x55, 0x1d,
 0x0f, 0x04, 0x04, 0x03, 0x02, 0x01, 0x86, 0x30,
 0x0f, 0x06, 0x03, 0x55, 0x1d, 0x13, 0x01, 0x01,
 0xff, 0x04, 0x05, 0x30, 0x03, 0x01, 0x01, 0xff,
 0x30, 0x1d, 0x06, 0x03, 0x55, 0x1d, 0x0e, 0x04,
 0x16, 0x04, 0x14, 0xd5, 0x67, 0x40, 0xe7, 0xe2,
 0x8e, 0x96, 0x60, 0xb1, 0xb7, 0xbc, 0x68, 0xe9,
 0x76, 0xc9, 0x0e, 0xa4, 0xe6, 0x90, 0x9a, 0x30,
 0x10, 0x06, 0x09, 0x2b, 0x06, 0x01, 0x04, 0x01,
 0x82, 0x37, 0x15, 0x01, 0x04, 0x03, 0x02, 0x01,
 0x00, 0x30, 0x0a, 0x06, 0x08, 0x2a, 0x86, 0x48,
 0xce, 0x3d, 0x04, 0x03, 0x02, 0x03, 0x47, 0x00,
 0x30, 0x44, 0x02, 0x20, 0x09, 0x7d, 0xce, 0x2f,
 0x1c, 0x93, 0xf9, 0x1f, 0x5f, 0x0f, 0xf5, 0x02,
 0x76, 0x7e, 0xa2, 0xf0, 0x5b, 0x1f, 0xc9, 0xe4,
 0x04, 0xae, 0x58, 0xf0, 0xd6, 0x3d, 0xea, 0x1a,
 0xf4, 0x81, 0x4d, 0x87, 0x02, 0x20, 0x0c, 0xd4,
 0xbd, 0x67, 0xa4, 0xf4, 0xd6, 0x3d, 0x52, 0xa5,
 0xbe, 0x6d, 0x66, 0x03, 0xc5, 0xb1, 0x29, 0x7e,
 0x9a, 0xb0, 0x19, 0x30, 0x69, 0x9d, 0x7d, 0x72,
 0xb7, 0x88, 0x3c, 0xb9, 0x94, 0x9b };

const uint8_t MBED_CLOUD_DEV_BOOTSTRAP_DEVICE_PRIVATE_KEY[] = 
{ 0x30, 0x81, 0x93, 0x02, 0x01, 0x00, 0x30, 0x13,
 0x06, 0x07, 0x2a, 0x86, 0x48, 0xce, 0x3d, 0x02,
 0x01, 0x06, 0x08, 0x2a, 0x86, 0x48, 0xce, 0x3d,
 0x03, 0x01, 0x07, 0x04, 0x79, 0x30, 0x77, 0x02,
 0x01, 0x01, 0x04, 0x20, 0xa6, 0x41, 0x3a, 0xe2,
 0x91, 0xf9, 0x25, 0xad, 0x97, 0x40, 0x28, 0x00,
 0xae, 0xb2, 0xbf, 0x59, 0xbf, 0xf7, 0xcb, 0x94,
 0x7d, 0x31, 0x2c, 0x37, 0x5a, 0x65, 0x8a, 0x98,
 0x7d, 0xeb, 0xe2, 0xfb, 0xa0, 0x0a, 0x06, 0x08,
 0x2a, 0x86, 0x48, 0xce, 0x3d, 0x03, 0x01, 0x07,
 0xa1, 0x44, 0x03, 0x42, 0x00, 0x04, 0xd5, 0xbf,
 0x56, 0x36, 0x59, 0x69, 0x71, 0x41, 0x3c, 0x73,
 0xe0, 0xad, 0x0f, 0x3b, 0x8c, 0xd8, 0xa2, 0x24,
 0xb1, 0x27, 0xfd, 0xf1, 0x9d, 0xb9, 0x78, 0x7b,
 0x38, 0x09, 0x25, 0x42, 0x3f, 0xaa, 0x3f, 0xc3,
 0x2c, 0x4c, 0xbe, 0x27, 0x27, 0xfb, 0xd8, 0x3d,
 0x94, 0x2e, 0x32, 0x7c, 0x9d, 0xd7, 0x51, 0x0b,
 0x4a, 0xaf, 0x8e, 0x25, 0xc4, 0x5e, 0x5c, 0x1b,
 0x73, 0x87, 0x1e, 0x88, 0x11, 0xa3 };

const char MBED_CLOUD_DEV_MANUFACTURER[] = "dev_manufacturer";

const char MBED_CLOUD_DEV_MODEL_NUMBER[] = "dev_model_num";

const char MBED_CLOUD_DEV_SERIAL_NUMBER[] = "0";

const char MBED_CLOUD_DEV_DEVICE_TYPE[] = "dev_device_type";

const char MBED_CLOUD_DEV_HARDWARE_VERSION[] = "dev_hardware_version";

const uint32_t MBED_CLOUD_DEV_MEMORY_TOTAL_KB = 0;

const uint32_t MBED_CLOUD_DEV_BOOTSTRAP_DEVICE_CERTIFICATE_SIZE = sizeof(MBED_CLOUD_DEV_BOOTSTRAP_DEVICE_CERTIFICATE);
const uint32_t MBED_CLOUD_DEV_BOOTSTRAP_SERVER_ROOT_CA_CERTIFICATE_SIZE = sizeof(MBED_CLOUD_DEV_BOOTSTRAP_SERVER_ROOT_CA_CERTIFICATE);
const uint32_t MBED_CLOUD_DEV_BOOTSTRAP_DEVICE_PRIVATE_KEY_SIZE = sizeof(MBED_CLOUD_DEV_BOOTSTRAP_DEVICE_PRIVATE_KEY);

#endif //__MBED_CLOUD_DEV_CREDENTIALS_H__
