import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  DataTable,
  TableContainer,
  Table,
  TableHead,
  TableRow,
  TableHeader,
  TableBody,
  TableCell,
  Button,
  Loading,
  InlineNotification
} from '@carbon/react';
import { Add, View } from '@carbon/icons-react';
import { bookingsAPI } from '../services/api';
import { format } from 'date-fns';
import './BookingList.scss';

const headers = [
  { key: 'booking_reference', header: 'Reference' },
  { key: 'customer_name', header: 'Customer' },
  { key: 'origin', header: 'Origin' },
  { key: 'destination', header: 'Destination' },
  { key: 'travel_date', header: 'Travel Date' },
  { key: 'total_cost', header: 'Total Cost' },
  { key: 'status', header: 'Status' },
  { key: 'actions', header: 'Actions' }
];

const BookingList = () => {
  const navigate = useNavigate();
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadBookings();
  }, []);

  const loadBookings = async () => {
    try {
      setLoading(true);
      const response = await bookingsAPI.getAll();
      setBookings(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load bookings');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    try {
      return format(new Date(dateString), 'MMM dd, yyyy');
    } catch {
      return dateString;
    }
  };

  const rows = bookings.map((booking) => ({
    id: booking.id.toString(),
    booking_reference: booking.booking_reference,
    customer_name: booking.customer_name,
    origin: booking.origin,
    destination: booking.destination,
    travel_date: formatDate(booking.travel_date),
    total_cost: `₹${booking.total_cost.toLocaleString('en-IN')}`,
    status: booking.status,
    actions: booking.id
  }));

  if (loading) {
    return <Loading description="Loading bookings..." withOverlay={false} />;
  }

  return (
    <div className="booking-list">
      <div className="page-header">
        <div>
          <h1>Travel Bookings</h1>
          <p>Manage and view all travel bookings</p>
        </div>
        <Button
          kind="primary"
          renderIcon={Add}
          onClick={() => navigate('/bookings/new')}
        >
          Create Booking
        </Button>
      </div>

      {error && (
        <InlineNotification
          kind="error"
          title="Error"
          subtitle={error}
          onCloseButtonClick={() => setError(null)}
        />
      )}

      <DataTable rows={rows} headers={headers}>
        {({ rows, headers, getTableProps, getHeaderProps, getRowProps }) => (
          <TableContainer title="All Bookings">
            <Table {...getTableProps()}>
              <TableHead>
                <TableRow>
                  {headers.map((header) => (
                    <TableHeader {...getHeaderProps({ header })} key={header.key}>
                      {header.header}
                    </TableHeader>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {rows.map((row) => (
                  <TableRow {...getRowProps({ row })} key={row.id}>
                    {row.cells.map((cell) => (
                      <TableCell key={cell.id}>
                        {cell.info.header === 'actions' ? (
                          <Button
                            kind="ghost"
                            size="sm"
                            renderIcon={View}
                            onClick={() => navigate(`/bookings/${cell.value}`)}
                          >
                            View Details
                          </Button>
                        ) : cell.info.header === 'status' ? (
                          <span className={`status-badge status-${cell.value}`}>
                            {cell.value}
                          </span>
                        ) : (
                          cell.value
                        )}
                      </TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </DataTable>

      {bookings.length === 0 && !loading && (
        <div className="empty-state">
          <p>No bookings found. Create your first booking to get started.</p>
          <Button
            kind="primary"
            renderIcon={Add}
            onClick={() => navigate('/bookings/new')}
          >
            Create First Booking
          </Button>
        </div>
      )}
    </div>
  );
};

export default BookingList;

// Made with Bob
