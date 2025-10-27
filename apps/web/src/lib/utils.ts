import { MIME_TYPES } from '@mantine/dropzone';
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Converts a given number of bytes into a human-readable string representation
 * with appropriate units (Bytes, KB, MB, GB, TB).
 *
 * @param bytes - The size in bytes to be converted.
 * @returns A string representing the size in a human-readable format.
 *          Returns "n/a" if the input is 0.
 *
 * @example
 * ```typescript
 * bytesToSize(1024); // "1.0 KB"
 * bytesToSize(1048576); // "1.0 MB"
 * bytesToSize(0); // "n/a"
 * ```
 */
export const bytesToSize = (bytes: number) => {
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  if (bytes == 0) return 'n/a';
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  if (i == 0) return bytes + ' ' + sizes[i];
  return (bytes / Math.pow(1024, i)).toFixed(1) + ' ' + sizes[i];
};

export const getFileIcon = (type: string) => {
  switch (type) {
    case MIME_TYPES.pdf:
      return 'mdi:file-pdf';
    case MIME_TYPES.docx:
      return 'mdi:file-word';
    case MIME_TYPES.csv:
      return 'mdi:file-csv';
    case MIME_TYPES.xlsx:
      return 'mdi:file-excel';
    default:
      return 'mdi:file-document';
  }
};
