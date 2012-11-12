// *****************************************************************************
// NICOS, the Networked Instrument Control System of the FRM-II
// Copyright (c) 2009-2012 by the NICOS contributors (see AUTHORS)
//
// This program is free software; you can redistribute it and/or modify it under
// the terms of the GNU General Public License as published by the Free Software
// Foundation; either version 2 of the License, or (at your option) any later
// version.
//
// This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
// details.
//
// You should have received a copy of the GNU General Public License along with
// this program; if not, write to the Free Software Foundation, Inc.,
// 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
//
// Module authors:
//   Tobias Weber <tweber@frm2.tum.de>
//
// *****************************************************************************

#include "fourier.h"
#include <math.h>
#include <string.h>
#include "logger.h"
#include "../config/globals.h"
#include "gc.h"
#include "helper.h"

#ifdef USE_FFTW
	#include <fftw3.h>
#endif


//------------------------------------------------------------------------------
// fft using fftw
#ifdef USE_FFTW

Fourier::Fourier(unsigned int iSize) : m_iSize(iSize)
{
	m_pIn = fftw_malloc(m_iSize * sizeof(fftw_complex));
	m_pOut = fftw_malloc(m_iSize * sizeof(fftw_complex));

	m_pPlan = gc.malloc(sizeof(fftw_plan), "fftw_plan");
	m_pPlan_inv = gc.malloc(sizeof(fftw_plan), "fftw_plan_inv");

	fftw_plan* pPlan = (fftw_plan*) m_pPlan;
	fftw_plan* pPlan_inv = (fftw_plan*) m_pPlan_inv;

	*pPlan = fftw_plan_dft_1d(iSize,
								(fftw_complex*)m_pIn, (fftw_complex*)m_pOut,
								FFTW_FORWARD, FFTW_MEASURE);

	*pPlan_inv = fftw_plan_dft_1d(iSize,
								(fftw_complex*)m_pIn, (fftw_complex*)m_pOut,
								FFTW_BACKWARD, FFTW_MEASURE);

	if(!*pPlan || !*pPlan_inv)
	{
		logger.SetCurLogLevel(LOGLEVEL_ERR);
		logger << "Fourier: Could not create plan.\n";
	}
}

Fourier::~Fourier()
{
	fftw_destroy_plan(*(fftw_plan*)m_pPlan);
	fftw_destroy_plan(*(fftw_plan*)m_pPlan_inv);

	gc.release(m_pPlan);
	gc.release(m_pPlan_inv);

	fftw_free(m_pIn);
	fftw_free(m_pOut);
}

bool Fourier::fft(const double* pRealIn, const double *pImagIn,
					double *pRealOut, double *pImagOut)
{
	fftw_plan* pPlan = (fftw_plan*) m_pPlan;

	fftw_complex* pIn = (fftw_complex*)m_pIn;
	fftw_complex* pOut = (fftw_complex*)m_pOut;

	for(unsigned int i=0; i<m_iSize; ++i)
	{
		pIn[i][0] = pRealIn[i];
		pIn[i][1] = pImagIn[i];

		pOut[i][0] = 0.;
		pOut[i][1] = 0.;
	}

	fftw_execute(*pPlan);

	for(unsigned int i=0; i<m_iSize; ++i)
	{
		pRealOut[i] = pOut[i][0];
		pImagOut[i] = pOut[i][1];
	}

	return true;
}

bool Fourier::ifft(const double* pRealIn, const double *pImagIn,
					double *pRealOut, double *pImagOut)
{
	fftw_plan* pPlan_inv = (fftw_plan*) m_pPlan_inv;

	fftw_complex* pIn = (fftw_complex*)m_pIn;
	fftw_complex* pOut = (fftw_complex*)m_pOut;

	for(unsigned int i=0; i<m_iSize; ++i)
	{
		pIn[i][0] = pRealIn[i];
		pIn[i][1] = pImagIn[i];

		pOut[i][0] = 0.;
		pOut[i][1] = 0.;
	}

	fftw_execute(*pPlan_inv);

	for(unsigned int i=0; i<m_iSize; ++i)
	{
		pRealOut[i] = pOut[i][0];
		pImagOut[i] = pOut[i][1];
	}

	return true;
}

#else	// !USE_FFTW

Fourier::Fourier(unsigned int iSize) : m_iSize(iSize)
{
	/*
	static bool bWarningShown = false;

	if(!bWarningShown)
	{
		logger.SetCurLogLevel(LOGLEVEL_WARN);
		logger << "Fourier: Not compiled with fftw, using some "
				  "not-nearly-as-cool (or fast) standard dft "
				  "calculations instead.\n";
		bWarningShown = true;
	}
	*/
}

Fourier::~Fourier()
{}

bool Fourier::fft(const double *pRealIn, const double *pImagIn,
					double *pRealOut, double *pImagOut)
{
	// if we don't have the fftw available, use dft instead
	dft<double>(pRealIn, pImagIn, pRealOut, pImagOut, m_iSize);

	return true;
}

bool Fourier::ifft(const double *pRealIn, const double *pImagIn,
					double *pRealOut, double *pImagOut)
{
	// if we don't have the fftw available, use dft instead
	idft<double>(pRealIn, pImagIn, pRealOut, pImagOut, m_iSize);

	return true;	
}

#endif	// USE_FFTW

bool Fourier::shift_sin(double dNumOsc, const double* pDatIn,
				double *pDataOut, double dPhase)
{
	unsigned int iSize = m_iSize;
	const double dSize = double(iSize);
	const int iNumOsc = int(dNumOsc);
	dNumOsc = double(iNumOsc);			// consider only full oscillations

	//double dShiftSamples = dPhase/(2.*M_PI) * dSize;

	double *pZero = new double[iSize];
	memset(pZero, 0, sizeof(double)*iSize);

	double *pDatFFT_real = new double[iSize];
	double *pDatFFT_imag = new double[iSize];

	autodeleter<double> _a0(pZero, true);
	autodeleter<double> _a1(pDatFFT_real, true);
	autodeleter<double> _a2(pDatFFT_imag, true);

	if(!fft(pDatIn, pZero, pDatFFT_real, pDatFFT_imag))
		return false;

	// filter out everything not concerning the sine with iNumOsc oscillations
	for(unsigned int i=0; i<iSize; ++i)
	{
		if(int(i)==iNumOsc || i==0)
			continue;

		pDatFFT_real[i] = 0.;
		pDatFFT_imag[i] = 0.;
	}

	// amp & phase
	std::complex<double> c(pDatFFT_real[iNumOsc], pDatFFT_imag[iNumOsc]);

	// since the signal is real we can take the first half of the fft data
	// and multiply by two.
	c *= 2.;
	c = ::phase_correction_0<double>(c, dPhase);

	pDatFFT_real[iNumOsc] = c.real();
	pDatFFT_imag[iNumOsc] = c.imag();

	// offset
	pDatFFT_imag[0] = 0.;


	if(!ifft(pDatFFT_real, pDatFFT_imag, pDataOut, pZero))
		return false;


	// normalization
	for(unsigned int i=0; i<iSize; ++i)
		pDataOut[i] /= double(iSize);

	//save_dat("in.dat", pDatIn, iSize);
	//save_dat("out.dat", pDataOut, iSize);
	return true;
}

bool Fourier::phase_correction_0(double dNumOsc, const double* pDatIn,
				double *pDataOut, double dPhase)
{
	unsigned int iSize = m_iSize;
	const double dSize = double(iSize);
	const int iNumOsc = int(dNumOsc);
	dNumOsc = double(iNumOsc);			// consider only full oscillations

	double *pZero = new double[iSize];
	memset(pZero, 0, sizeof(double)*iSize);

	double *pDatFFT_real = new double[iSize];
	double *pDatFFT_imag = new double[iSize];

	autodeleter<double> _a0(pZero, true);
	autodeleter<double> _a1(pDatFFT_real, true);
	autodeleter<double> _a2(pDatFFT_imag, true);

	if(!fft(pDatIn, pZero, pDatFFT_real, pDatFFT_imag))
		return false;

	for(unsigned int i=1; i<iSize; ++i)
	{
		std::complex<double> c(pDatFFT_real[i], pDatFFT_imag[i]);
		if(i<iSize/2)
		{
			c *= 2.;
			c = ::phase_correction_0<double>(c, dPhase*double(i));
		}
		else
		{
			// not needed in real input data
			c = std::complex<double>(0., 0.);
		}

		pDatFFT_real[i] = c.real();
		pDatFFT_imag[i] = c.imag();
	}

	if(!ifft(pDatFFT_real, pDatFFT_imag, pDataOut, pZero))
		return false;

	// normalization
	for(unsigned int i=0; i<iSize; ++i)
		pDataOut[i] /= double(iSize);

	//save_dat("in.dat", pDatIn, iSize);
	//save_dat("out.dat", pDataOut, iSize);
	return true;
}

bool Fourier::phase_correction_1(double dNumOsc, const double* pDatIn,
				double *pDataOut, double dPhaseOffs, double dPhaseSlope)
{
	unsigned int iSize = m_iSize;
	const double dSize = double(iSize);
	const int iNumOsc = int(dNumOsc);
	dNumOsc = double(iNumOsc);			// consider only full oscillations

	double *pZero = new double[iSize];
	memset(pZero, 0, sizeof(double)*iSize);

	double *pDatFFT_real = new double[iSize];
	double *pDatFFT_imag = new double[iSize];

	autodeleter<double> _a0(pZero, true);
	autodeleter<double> _a1(pDatFFT_real, true);
	autodeleter<double> _a2(pDatFFT_imag, true);

	if(!fft(pDatIn, pZero, pDatFFT_real, pDatFFT_imag))
		return false;

	for(unsigned int i=1; i<iSize; ++i)
	{
		std::complex<double> c(pDatFFT_real[i], pDatFFT_imag[i]);
		if(i<iSize/2)
		{
			double dX = double(i)/double(iSize);
			
			c *= 2.;
			c = ::phase_correction_1<double>(c, dPhaseOffs*double(i), 
								dPhaseSlope*double(i), dX);
		}
		else
		{
			// not needed in real input data
			c = std::complex<double>(0., 0.);
		}

		pDatFFT_real[i] = c.real();
		pDatFFT_imag[i] = c.imag();
	}

	if(!ifft(pDatFFT_real, pDatFFT_imag, pDataOut, pZero))
		return false;

	// normalization
	for(unsigned int i=0; i<iSize; ++i)
		pDataOut[i] /= double(iSize);

	//save_dat("in.dat", pDatIn, iSize);
	//save_dat("out.dat", pDataOut, iSize);
	return true;
}


bool Fourier::get_contrast(double dNumOsc, const double* pDatIn,
						   double& dC, double& dPh)
{
	unsigned int iSize = m_iSize;
	const double dSize = double(iSize);
	const int iNumOsc = int(dNumOsc);
	dNumOsc = double(iNumOsc);			// consider only full oscillations

	double *pZero = new double[iSize];
	memset(pZero, 0, sizeof(double)*iSize);

	double *pDatFFT_real = new double[iSize];
	double *pDatFFT_imag = new double[iSize];

	autodeleter<double> _a0(pZero, true);
	autodeleter<double> _a1(pDatFFT_real, true);
	autodeleter<double> _a2(pDatFFT_imag, true);

	if(!fft(pDatIn, pZero, pDatFFT_real, pDatFFT_imag))
		return false;

	double dReal = 2.*pDatFFT_real[iNumOsc]/double(m_iSize);
	double dImag = 2.*pDatFFT_imag[iNumOsc]/double(m_iSize);

	double dAmp = sqrt(dReal*dReal + dImag*dImag);
	double dOffs = pDatFFT_real[0] / double(m_iSize);

	//std::cout << "amp = " << dAmp << std::endl;
	//std::cout << "offs = " << dOffs << std::endl;

	dC = dAmp/dOffs;
	dPh = atan2(dImag, dReal) + M_PI/2.;

	// half of first bin
	//dPh += - 0.5/dNumOsc * 2.*M_PI;

	if(dPh<0.)
		dPh += 2.*M_PI;

	return true;
}
//------------------------------------------------------------------------------


/*
// Test
#include <fstream>
#include <iostream>

int main()
{
	const int N = 64;
	Fourier fourier(N);

	double dIn[N];
	double dOut[N];

	double dAmp = 2.333;
	double dOffs = 5.123;

	for(int i=0; i<N; ++i)
		dIn[i] = dAmp*sin(2.* double(i+0.5)/double(N) * 2.*M_PI) + dOffs;

	fourier.shift_sin(2., dIn, dOut, M_PI/4.);

	for(int i=0; i<N; ++i)
		std::cout << dOut[i] << " ";
	std::cout << std::endl;


	double dC, dPh;
	fourier.get_contrast(2., dIn, dC, dPh);
	std::cout << "contrast = " << dC << std::endl;

	return 0;
}
*/
