/*
 *   TOP2049 Open Source programming suite
 *
 *   Universal device tester
 *   FPGA bottomhalf implementation
 *
 *   Copyright (c) 2010 Michael Buesch <mb@bu3sch.de>
 *
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation; either version 2 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License along
 *   with this program; if not, write to the Free Software Foundation, Inc.,
 *   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 */

/* The runtime ID and revision. */
`define RUNTIME_ID	16'h0008
`define RUNTIME_REV	16'h01

module unitest(data, ale, write, read, zif);
	inout [7:0] data;
	input ale;
	input write;
	input read;
	inout [48:1] zif;

	/* Interface to the microcontroller */
	wire read_oe;		/* Read output-enable */
	reg [7:0] address;	/* Cached address value */
	reg [7:0] read_data;	/* Cached read data */

	/* ZIF pin controls */
	reg [47:0] zif_output_en;
	reg [47:0] zif_output;

	initial begin
		zif_output_en <= 0;
		zif_output <= 0;
	end

	always @(posedge write) begin
		case (address)
		8'h10: begin
			/* Data write */
			/* Unused */
		end
		8'h12: begin
			zif_output_en[7:0] <= data;
		end
		8'h13: begin
			zif_output_en[15:8] <= data;
		end
		8'h14: begin
			zif_output_en[23:16] <= data;
		end
		8'h15: begin
			zif_output_en[31:24] <= data;
		end
		8'h16: begin
			zif_output_en[39:32] <= data;
		end
		8'h17: begin
			zif_output_en[47:40] <= data;
		end
		8'h18: begin
			zif_output[7:0] <= data;
		end
		8'h19: begin
			zif_output[15:8] <= data;
		end
		8'h1A: begin
			zif_output[23:16] <= data;
		end
		8'h1B: begin
			zif_output[31:24] <= data;
		end
		8'h1C: begin
			zif_output[39:32] <= data;
		end
		8'h1D: begin
			zif_output[47:40] <= data;
		end
		endcase
	end

	always @(negedge read) begin
		case (address)
		8'h10: begin
			/* Data read */
			/* Unused */
		end
		8'h18: begin
			read_data <= zif[8:1];
		end
		8'h19: begin
			read_data <= zif[16:9];
		end
		8'h1A: begin
			read_data <= zif[24:17];
		end
		8'h1B: begin
			read_data <= zif[32:25];
		end
		8'h1C: begin
			read_data <= zif[40:33];
		end
		8'h1D: begin
			read_data <= zif[48:41];
		end

		8'hFD: read_data <= `RUNTIME_ID & 16'hFF;
		8'hFE: read_data <= (`RUNTIME_ID >> 8) & 16'hFF;
		8'hFF: read_data <= `RUNTIME_REV;
		endcase
	end

	always @(negedge ale) begin
		address <= data;
	end

	assign read_oe = !read && address[4];

	bufif1(zif[1], zif_output[0], zif_output_en[0]);
	bufif1(zif[2], zif_output[1], zif_output_en[1]);
	bufif1(zif[3], zif_output[2], zif_output_en[2]);
	bufif1(zif[4], zif_output[3], zif_output_en[3]);
	bufif1(zif[5], zif_output[4], zif_output_en[4]);
	bufif1(zif[6], zif_output[5], zif_output_en[5]);
	bufif1(zif[7], zif_output[6], zif_output_en[6]);
	bufif1(zif[8], zif_output[7], zif_output_en[7]);
	bufif1(zif[9], zif_output[8], zif_output_en[8]);
	bufif1(zif[10], zif_output[9], zif_output_en[9]);
	bufif1(zif[11], zif_output[10], zif_output_en[10]);
	bufif1(zif[12], zif_output[11], zif_output_en[11]);
	bufif1(zif[13], zif_output[12], zif_output_en[12]);
	bufif1(zif[14], zif_output[13], zif_output_en[13]);
	bufif1(zif[15], zif_output[14], zif_output_en[14]);
	bufif1(zif[16], zif_output[15], zif_output_en[15]);
	bufif1(zif[17], zif_output[16], zif_output_en[16]);
	bufif1(zif[18], zif_output[17], zif_output_en[17]);
	bufif1(zif[19], zif_output[18], zif_output_en[18]);
	bufif1(zif[20], zif_output[19], zif_output_en[19]);
	bufif1(zif[21], zif_output[20], zif_output_en[20]);
	bufif1(zif[22], zif_output[21], zif_output_en[21]);
	bufif1(zif[23], zif_output[22], zif_output_en[22]);
	bufif1(zif[24], zif_output[23], zif_output_en[23]);
	bufif1(zif[25], zif_output[24], zif_output_en[24]);
	bufif1(zif[26], zif_output[25], zif_output_en[25]);
	bufif1(zif[27], zif_output[26], zif_output_en[26]);
	bufif1(zif[28], zif_output[27], zif_output_en[27]);
	bufif1(zif[29], zif_output[28], zif_output_en[28]);
	bufif1(zif[30], zif_output[29], zif_output_en[29]);
	bufif1(zif[31], zif_output[30], zif_output_en[30]);
	bufif1(zif[32], zif_output[31], zif_output_en[31]);
	bufif1(zif[33], zif_output[32], zif_output_en[32]);
	bufif1(zif[34], zif_output[33], zif_output_en[33]);
	bufif1(zif[35], zif_output[34], zif_output_en[34]);
	bufif1(zif[36], zif_output[35], zif_output_en[35]);
	bufif1(zif[37], zif_output[36], zif_output_en[36]);
	bufif1(zif[38], zif_output[37], zif_output_en[37]);
	bufif1(zif[39], zif_output[38], zif_output_en[38]);
	bufif1(zif[40], zif_output[39], zif_output_en[39]);
	bufif1(zif[41], zif_output[40], zif_output_en[40]);
	bufif1(zif[42], zif_output[41], zif_output_en[41]);
	bufif1(zif[43], zif_output[42], zif_output_en[42]);
	bufif1(zif[44], zif_output[43], zif_output_en[43]);
	bufif1(zif[45], zif_output[44], zif_output_en[44]);
	bufif1(zif[46], zif_output[45], zif_output_en[45]);
	bufif1(zif[47], zif_output[46], zif_output_en[46]);
	bufif1(zif[48], zif_output[47], zif_output_en[47]);

	bufif1(data[0], read_data[0], read_oe);
	bufif1(data[1], read_data[1], read_oe);
	bufif1(data[2], read_data[2], read_oe);
	bufif1(data[3], read_data[3], read_oe);
	bufif1(data[4], read_data[4], read_oe);
	bufif1(data[5], read_data[5], read_oe);
	bufif1(data[6], read_data[6], read_oe);
	bufif1(data[7], read_data[7], read_oe);
endmodule
